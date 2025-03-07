#!/usr/bin/env python3

import rospy
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
import time

class DistanceCalculator:
    def __init__(self):
        rospy.init_node("distance_calculator", anonymous=True)

        # Subscriber ke topik /odom untuk posisi TurtleBot3
        rospy.Subscriber("/odom", Odometry, self.odom_callback)
        
        # Subscriber ke /move_base_simple/goal untuk mendapatkan tujuan navigasi
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, self.goal_callback)
        
        # Subscriber ke /amcl_pose untuk mendapatkan posisi akhir robot setelah navigasi selesai
        rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.amcl_callback)
        
        self.x_prev = None
        self.y_prev = None
        self.x_start = None  # Posisi awal robot
        self.y_start = None  # Posisi awal robot
        self.total_distance = 0.0  # Total jarak tempuh
        self.start_time = None
        self.goal_x = None
        self.goal_y = None
        self.end_x = None
        self.end_y = None

        rospy.loginfo("Node Distance Calculator telah dimulai.")
        rospy.spin()

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        
        # Menyimpan koordinat awal hanya sekali, saat pertama kali menerima data
        if self.x_start is None or self.y_start is None:
            self.x_start = x
            self.y_start = y
            rospy.loginfo(f"Posisi Awal Terekam: x={self.x_start:.2f}, y={self.y_start:.2f}")
        
        # Menyimpan koordinat sebelumnya jika tidak ada data sebelumnya
        if self.x_prev is None or self.y_prev is None:
            self.x_prev = x
            self.y_prev = y
            return

        # Menghitung jarak Euclidean antara titik sebelumnya dan saat ini
        distance = math.sqrt((x - self.x_prev) ** 2 + (y - self.y_prev) ** 2)
        self.total_distance += distance

        # rospy.loginfo(f"Koordinat Sekarang: x={x:.2f}, y={y:.2f}")
        # rospy.loginfo(f"Jarak dari Titik Sebelumnya: {distance:.4f} meter")
        # rospy.loginfo(f"Total Jarak Tempuh: {self.total_distance:.4f} meter\n")

        # Memperbarui koordinat sebelumnya
        self.x_prev = x
        self.y_prev = y

    def goal_callback(self, msg):
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.start_time = time.time()  # Catat waktu mulai navigasi
        rospy.loginfo(f"Tujuan Navigasi: x={self.goal_x:.2f}, y={self.goal_y:.2f}")

    def amcl_callback(self, msg):
        self.end_x = msg.pose.pose.position.x
        self.end_y = msg.pose.pose.position.y
        end_time = time.time()  # Catat waktu akhir navigasi
        
        if self.goal_x is not None and self.goal_y is not None:
            error_x = abs(self.goal_x - self.end_x) * 100  # Konversi ke cm
            error_y = abs(self.goal_y - self.end_y) * 100
            error_total = math.sqrt(error_x**2 + error_y**2)
            
            time_taken = end_time - self.start_time
            avg_speed = self.total_distance / time_taken if time_taken > 0 else 0
            
            rospy.loginfo("===== DATA NAVIGASI =====")
            rospy.loginfo(f"Posisi Awal: x={self.x_start:.2f}, y={self.y_start:.2f}")  # Menggunakan posisi awal yang benar
            rospy.loginfo(f"Posisi Tujuan: x={self.goal_x:.2f}, y={self.goal_y:.2f}")
            rospy.loginfo(f"Posisi Akhir: x={self.end_x:.2f}, y={self.end_y:.2f}")
            rospy.loginfo(f"Jarak Tempuh: {self.total_distance:.2f} meter")
            rospy.loginfo(f"Waktu Tempuh: {time_taken:.2f} detik")
            rospy.loginfo(f"Kecepatan Rata-rata: {avg_speed:.2f} m/s")
            rospy.loginfo(f"Kesalahan Navigasi: {error_total:.2f} cm")
            rospy.loginfo("=========================")

if __name__ == "__main__":
    try:
        DistanceCalculator()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node Distance Calculator dihentikan.")