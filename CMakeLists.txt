cmake_minimum_required(VERSION 2.6)
project(NemoAdmin NONE)
find_package(Gettext REQUIRED)

# Configurable paths
set(NEMO_PATH "/usr/bin/nemo" CACHE FILEPATH "nemo program path.")
set(XED_PATH "/usr/bin/xed" CACHE FILEPATH "xed program path.")

# Configure files
configure_file(extension/nemo-extension-admin.py
               extension/nemo-extension-admin.py)

# Update and compile the translations
file(GLOB TRANSLATION_FILES RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "po/*.po")
foreach(trans_file ${TRANSLATION_FILES})
    configure_file(${trans_file} ${trans_file} COPYONLY)
endforeach()
file(GLOB PO_FILES "${CMAKE_CURRENT_BINARY_DIR}/po/*.po")

# Add custom command to generate nemo-admin.pot
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/po/nemo-extension-admin.pot
    COMMAND xgettext --output=${CMAKE_CURRENT_BINARY_DIR}/po/nemo-extension-admin.pot ${CMAKE_CURRENT_SOURCE_DIR}/extension/nemo-extension-admin.py
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/extension/nemo-extension-admin.py
)

# Create translations
gettext_create_translations("${CMAKE_CURRENT_BINARY_DIR}/po/nemo-extension-admin.pot"
                            ALL ${PO_FILES})

# Ensure the locale directory exists
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/locale/ko/LC_MESSAGES)

# Generate .mo files for nemo-admin domain
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/locale/ko/LC_MESSAGES/nemo-extension-admin.mo
    COMMAND msgfmt ${CMAKE_CURRENT_BINARY_DIR}/po/ko.po -o ${CMAKE_CURRENT_BINARY_DIR}/locale/ko/LC_MESSAGES/nemo-extension-admin.mo
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/po/ko.po
)

add_custom_target(translations_nemo_extension_admin ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/locale/ko/LC_MESSAGES/nemo-extension-admin.mo
)

# Install target
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/extension/nemo-extension-admin.py"
        DESTINATION /usr/share/nemo-python/extensions)

# Install nemo-admin .mo file
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/locale/ko/LC_MESSAGES/nemo-extension-admin.mo"
        DESTINATION /usr/share/locale/ko/LC_MESSAGES)

# Uninstall target
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
               "${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake" IMMEDIATE @ONLY)
add_custom_target(uninstall COMMAND ${CMAKE_COMMAND}
                  -P ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake)

# Install the appdata file
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/nemo-extension-admin.appdata.xml
        DESTINATION share/metainfo)

