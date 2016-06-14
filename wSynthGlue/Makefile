all: wSynthGlue

wSynthGlue: main.o
	g++ main.o -o wSynthGlue

main.o: main.cpp
	g++ -c main.cpp

clean:
	rm *o wSynthGlue
