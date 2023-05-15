program= huamaker.elf
SRC=src/CPrinter.cpp src/CHuamaker.cpp src/main.cpp
HEAD=h

CC=g++
CPPFLAGS= -pedantic -Wall

.PHONY: build
.PHONY: clean

build:
	${CC} ${CPPFLAGS} ${SRC} -I${HEAD} -o ${program}

clean:
	rm -f *.o *.~ ${program}
