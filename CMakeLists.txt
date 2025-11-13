cmake_minimum_required(VERSION 3.8)
project(tortoisebot_gazebo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

# Install Python scripts with executable permissions
install(PROGRAMS
  scripts/closest_object_detector.py
  scripts/ball_follower.py
  scripts/sensor_fusion_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install directories
install(DIRECTORY
  worlds
  launch
  scripts
  config
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()