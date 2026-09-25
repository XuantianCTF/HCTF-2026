cmake_minimum_required(VERSION 3.22.1)
project(unrooted LANGUAGES CXX)

add_library(unrooted SHARED native-check.cpp)

target_compile_features(unrooted PRIVATE cxx_std_17)
target_compile_options(unrooted PRIVATE -Wall -Wextra -fvisibility=hidden)
