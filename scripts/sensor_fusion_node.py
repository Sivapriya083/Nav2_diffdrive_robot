#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2, PointField
import sensor_msgs_py.point_cloud2 as pc2
from std_msgs.msg import Header
import math

class SimpleSensorFusion(Node):
    def __init__(self):
        super().__init__('simple_sensor_fusion')
        
        # Subscribers
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.depth_sub = self.create_subscription(PointCloud2, '/camera/depth/color/points', self.depth_callback, 10)
        
        # Publisher
        self.fused_pub = self.create_publisher(PointCloud2, '/fused_pointcloud', 10)
        
        # Store latest data
        self.latest_scan = None
        self.latest_depth = None
        
        # Timer to fuse data (10 Hz)
        self.timer = self.create_timer(0.1, self.fuse_data)
        
        self.get_logger().info('Simple Sensor Fusion started')
        
    def scan_callback(self, msg):
        self.latest_scan = msg
        
    def depth_callback(self, msg):
        self.latest_depth = msg
        
    def fuse_data(self):
        """Combine LIDAR and depth camera data"""
        if self.latest_scan is None or self.latest_depth is None:
            return
            
        all_points = []
        
        # Convert LIDAR scan to points
        lidar_points = self.scan_to_points(self.latest_scan)
        all_points.extend(lidar_points)
        
        # Get depth camera points
        depth_points = self.get_depth_points(self.latest_depth)
        all_points.extend(depth_points)
        
        # Publish combined point cloud
        if all_points:
            self.publish_pointcloud(all_points)
            self.get_logger().info(f'Published {len(all_points)} fused points (LIDAR: {len(lidar_points)}, Depth: {len(depth_points)})')
    
    def scan_to_points(self, scan):
        """Convert LaserScan to 3D points"""
        points = []
        angle = scan.angle_min
        
        for distance in scan.ranges:
            if not math.isnan(distance) and not math.isinf(distance):
                if scan.range_min < distance < scan.range_max:
                    # Convert to x,y coordinates (z=0.1 for LIDAR height)
                    x = distance * math.cos(angle)
                    y = distance * math.sin(angle)
                    z = 0.1  # LIDAR is slightly above ground
                    points.append([x, y, z])
            angle += scan.angle_increment
            
        return points
    
    def get_depth_points(self, pointcloud):
        """Extract points from depth camera"""
        points = []
        valid_points = 0
        filtered_points = 0
        
        try:
            for point in pc2.read_points(pointcloud, field_names=("x", "y", "z"), skip_nans=True):
                x, y, z = point[0], point[1], point[2]
                valid_points += 1
                
                # FIXED: Only accept points ABOVE the robot (positive Z)
                # and within reasonable horizontal range
                if abs(x) < 3.0 and abs(y) < 3.0 and 0.05 < z < 2.5:  # z must be positive!
                    points.append([x, y, z])
                    filtered_points += 1
                    
        except Exception as e:
            self.get_logger().warn(f"Error processing depth points: {e}")
            
        if valid_points > 0:
            self.get_logger().debug(f"Depth camera: {valid_points} valid points, {filtered_points} passed filter")
            
        return points
        
    def publish_pointcloud(self, points):
        """Publish the fused point cloud"""
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = 'base_footprint'
        
        # Define point fields
        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]
        
        # Create and publish point cloud
        cloud = pc2.create_cloud(header, fields, points)
        self.fused_pub.publish(cloud)

def main():
    rclpy.init()
    node = SimpleSensorFusion()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()