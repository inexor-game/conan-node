cmake_minimum_required( VERSION 2.8.12 )
project( PackageTest )

include( ${CMAKE_BINARY_DIR}/conanbuildinfo.cmake )
conan_basic_setup()

if (APPLE)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -stdlib=libc++")
endif ()

add_executable( example example.cpp )

target_link_libraries( example ${CONAN_LIBS} )

# Need to change install_name of libnode.dylib because the default is /usr/local/lib/libnode.dylib
add_custom_command(TARGET example POST_BUILD COMMAND install_name_tool -change /usr/local/lib/libnode.dylib ${CONAN_LIB_DIRS_NODE}/libnode.dylib $<TARGET_FILE:example>)