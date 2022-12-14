#include <sstream>
#include <string>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

void parsec_roi_begin() 
{

}

void parsec_roi_end() 
{

}

vector< vector<int> > read(string filename) {
	vector< vector<int> > inputMatrix;
	string line;
	ifstream infile;
	infile.open (filename.c_str());

	int i = 0;
	while (getline(infile, line) && !line.empty()) {
		istringstream iss(line);
		inputMatrix.resize(inputMatrix.size() + 1);
		int a, j = 0;
		while (iss >> a) {
			inputMatrix[i].push_back(a);
			j++;
		}
		i++;
	}

	infile.close();
	return inputMatrix;
}

vector< vector<int> > transpose(vector< vector<int> > inputMatrix) {
	if (inputMatrix.size() == 0)
        return inputMatrix;
	vector< vector<int> > transVector (inputMatrix[0].size(), vector<int>());
	for (size_t i = 0; i < inputMatrix[0].size(); i++) {
		for (size_t j = 0; j < inputMatrix[i].size(); j++) {
				transVector[j].push_back(inputMatrix[i][j]);
			}
		}
	return transVector;
}

void printMatrix(vector< vector<int> > matrix) {
	vector< vector<int> >::iterator it;
	vector<int>::iterator inner;
	for (it=matrix.begin(); it != matrix.end(); it++) {
		for (inner = it->begin(); inner != it->end(); inner++) {
			cout << *inner;
			if(inner+1 != it->end()) {
				cout << "\t";
			}
		}
		cout << endl;
	}
}

int main (int argc, char* argv[]) {
	string filename;
	if (argc < 3) {
		filename = "2000.in";
	} else {
		filename = argv[2];
	}
	vector< vector<int> > inputMatrix = read (filename);
    parsec_roi_begin();
	vector< vector<int> > transVector = transpose(inputMatrix);
    parsec_roi_end();
	printMatrix(transVector);
	return 0;
}