#include <iostream>
#include <fstream>
#include <cstdlib>
#include <time.h>
using namespace std;

int main() {
	int iteration;
	cin >> iteration;
	
	string name;
	cin >> name;
	
	char *charPath = const_cast<char*>(name.c_str());
	ofstream randOut(charPath);
	
	for (int i=0; i<iteration; ++i) {
		randOut << i << endl;
	}
	
	randOut.close();
	
	return 0;
}
