cmake_minimum_required(VERSION 2.8)
project(laser_cam)

find_package(OpenCV REQUIRED)
include_directories( ${OpenCV_INCLUDE_DIRS})
add_executable(main cap_test.cpp )
add_executable(test test.cpp simple-serial-port/SimpleSerial.cpp)
add_executable(laser_cam main.cpp simple-serial-port/SimpleSerial.cpp)

target_link_libraries(main ${OpenCV_LIBS})
target_link_libraries(laser_cam ${OpenCV_LIBS})

