import os
import jinja2
import shutil
from pathlib import Path
from consolemenu import ConsoleMenu
from consolemenu.items import ExitItem
from consolemenu.items import FunctionItem


cmake_template = """project({{name}})
cmake_minimum_required(VERSION 3.00)

SET(GCC_COVERAGE_COMPILE_FLAGS "-g -O0 -coverage -fprofile-arcs -ftest-coverage")
SET(GCC_COVERAGE_LINK_FLAGS    "-coverage -lgcov")
SET( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS} -std=c++11 -Wall -Wno-unknown-pragmas -Werror -pedantic")
SET( CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS} -Wall -Wno-unknown-pragmas -Werror -pedantic")
SET(CMAKE_CXX_OUTPUT_EXTENSION_REPLACE ON)
SET(CMAKE_C_OUTPUT_EXTENSION_REPLACE ON)
SET(CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}" )

SET(PROJECT_DIR {{project_dir}})

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_USE_RESPONSE_FILE_FOR_INCLUDES Off)
# SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -include MemLeakDetectionNewMacros.h")
# SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -include MemLeakDetectionMallocMacros.h")
# SET(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -include MemLeakDetectionMallocMacros.h")

add_executable(TestApp
    {% for file in sut_code -%}
        ${CMAKE_SOURCE_DIR}/{{file}}        
    {% endfor %}
	${CMAKE_SOURCE_DIR}/{{code}}
	${CMAKE_SOURCE_DIR}/main.cpp
	)

SET(CPPCHECK_LIB "C:/Users/Z00436NS/mtdd/BitInverter/cpputest")

include_directories(
    {% for dir in includes -%}
        ${PROJECT_DIR}/{{dir}}
    {% endfor %}
	${CPPCHECK_LIB}/include
    )

{% if os_name == 'nt' %}
    find_library(TestLib    libCppUTest ${CPPCHECK_LIB}/mingw)
    find_library(TestLibExt libCppUTestExt ${CPPCHECK_LIB}/mingw)
    target_link_libraries(TestApp ${TestLib} ${TestLibExt})
{% else %}
    target_link_libraries(TestApp CppUTest CppUTestExt)
{% endif %}
"""

main_template = """
#include "CppUTest/CommandLineTestRunner.h"
#include "CppUTest/TestPlugin.h"
#include "CppUTest/TestRegistry.h"
#include "CppUTestExt/IEEE754ExceptionsPlugin.h"
#include "CppUTestExt/MockSupportPlugin.h"

class MyDummyComparator : public MockNamedValueComparator
{
public:
    virtual bool isEqual(const void* object1, const void* object2)
    {
        return object1 == object2;
    }

    virtual SimpleString valueToString(const void* object)
    {
        return StringFrom(object);
    }
};

int main(int ac, char** av)
{
    MyDummyComparator dummyComparator;
    MockSupportPlugin mockPlugin;
    IEEE754ExceptionsPlugin ieee754Plugin;

    mockPlugin.installComparator("MyDummyType", dummyComparator);
    TestRegistry::getCurrentRegistry()->installPlugin(&mockPlugin);
    TestRegistry::getCurrentRegistry()->installPlugin(&ieee754Plugin);
    return CommandLineTestRunner::RunAllTests(ac, av);
}
"""


def bash_exec(root, cmd):
    saved_path = os.getcwd()
    os.chdir(root)
    print(cmd)
    os.system(cmd)
    os.chdir(saved_path)

class TDD:
    def __init__(self):
        self.project = Path()
        self.tests = []
        self.includes = []
        if os.name == 'nt':
            self.makefile = "MinGW Makefiles"
        else:
            self.makefile = "Unix Makefiles"
    
    def test(self, test_file):
        test = Test(test_file, self)
        self.tests.append(test)
        return test

    def menu(self):
        menu = ConsoleMenu("eTDD is C++ unit test framework. (%s)" % ("opa"),
                            "Choose test packag/es variant.", show_exit_option=False)
        menu.append_item( ExitItem("Auf wiedersehen!!", menu=None) )
        for test in self.tests:
            menu.append_item( FunctionItem(test.name, test.run_all, [])  )
        menu.show()


class Test:
    def __init__(self, test_file: str, tdd: TDD):
        self.name = Path(test_file).stem
        self.code = test_file
        self.sut = []
        self.home = Path("tmp") / self.name
        self.build = self.home / "build"
        self.tdd = tdd
        self.includes = []

    def generate(self, template_text, filename, **data):
        rtemplate = jinja2.Environment().from_string(template_text)
        rendered = rtemplate.render(**data)
        with open(self.home / filename, "w") as fd:
            fd.write(rendered)

    def copy(self):
        code_name = Path(self.code).name
        project_path = Path(self.tdd.project)
        os.makedirs(self.home, exist_ok=True)
        self.generate(main_template, "main.cpp")
        shutil.copyfile( project_path / self.code, self.home / Path(self.code).name)

        test_sut_code = []
        for file in self.sut:
            filename = Path(file).name
            shutil.copyfile( project_path / file, self.home / filename )
            file_suffix = Path(filename).suffix
            if file_suffix == '.c' or file_suffix == '.cpp':
                test_sut_code.append(filename)

        includes = []
        includes += self.tdd.includes
        includes += self.includes

        project_dir = str(self.tdd.project.resolve()).replace("\\","\\\\")
        self.generate(cmake_template, "CMakeLists.txt", name=self.name, project_dir=project_dir, code=code_name, sut_code=test_sut_code, os_name=os.name, includes=includes)


    def configure(self):
        os.makedirs(self.build, exist_ok=True)
        bash_exec(self.build, 'cmake -G "{}" ..'.format(self.tdd.makefile))

    def make(self):
        bash_exec(self.build, 'make')

    def exec(self):
        if os.name == 'nt':
            bash_exec(self.build, 'TestApp')
        else:
            bash_exec(self.build, './TestApp')

    def cppcheck(self):
        # cppcheck
        pass

    def coverage(self):
        """
            # gcovr --object-directory CMakeFiles\TestApp.dir\mingw_tmp_single -r ..\mingw_tmp_single\ -f "\.\./mingw_tmp_single/Calculator.cpp" -b --txt cov_vypis.txt --html cov\cov_html.html --html-details cov\coverage_details.html
        """

        bash_exec(self.build, 'gcovr --object-directory CMakeFiles\TestApp.dir\\ -r ..\\ -f "..\\ut_BitInverter.cpp" -b --txt cov_vypis.txt --html cov\\cov_html.html --html-details cov\\coverage_details.html')

    def complexity(self):
        files = []
        for file in self.sut:
            files.append( Path(file).name )
        files_str = ' '.join(files)
        bash_exec(self.home, "lizard {}".format(files_str))

    def run_all(self):
        self.copy()
        self.cppcheck()
        self.configure()
        self.make()
        self.exec()
        # self.complexity()
        # self.coverage()
        if os.name == 'nt':
            os.system("pause")
        else:
            input('Press <ENTER> to continue')
