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


struct Result {
	vector< vector<int> > inputData;
	vector< vector<int> > gatherIndexVector;
	vector< vector<int> > scatterIndexVector;
	vector< int > gatherMatrix;

};

Result read(string filename) {
	vector< vector<int> > inputData, gatherIndexVector, scatterIndexVector;
	vector< int > gatherMatrix;
	Result gatherInput;
	string line;
	ifstream infile;
	infile.open (filename.c_str());

	int i = 0;
	while (getline(infile, line) && !line.empty()) {
		istringstream iss(line);
		inputData.resize(inputData.size() + 1);
		int a, j = 0;
		while (iss >> a) {
			inputData[i].push_back(a);
			j++;
		}
		i++;
	}

	i = 0;
	while (getline(infile, line)) {
		istringstream iss(line);
		gatherIndexVector.resize(gatherIndexVector.size() + 1);
		int a;
		int j = 0;
		while (iss >> a) {
			gatherIndexVector[i].push_back(a);
			j++;
		}
		i++;
	}

	i = 0;
	while (getline(infile, line)) {
		istringstream iss(line);
		scatterIndexVector.resize(scatterIndexVector.size() + 1);
		int a;
		int j = 0;
		while (iss >> a) {
			scatterIndexVector[i].push_back(a);
			j++;
		}
		i++;
	}

	i = 0;
	while (getline(infile, line)) {
		istringstream iss(line);
		gatherMatrix.resize(gatherMatrix.size() + 1);
		int a;
		// int j = 0;
		while (iss >> a) {
			gatherMatrix.push_back(a);
			// j++;
		}
		i++;
	}

	infile.close();
	gatherInput.inputData = inputData;
	gatherInput.gatherIndexVector = gatherIndexVector;
	gatherInput.scatterIndexVector = scatterIndexVector;
	gatherInput.gatherMatrix = gatherMatrix;
	return gatherInput;
}

vector< vector<int> > scatter(vector< vector<int> > inputData,
									vector< vector<int> > scatterIndexVector, vector< int> gatherMatrix) {
	int n = inputData.size();
	int indexN = scatterIndexVector.size();
 	cout <<"size of scatterIndexVector "<<indexN<<endl; 
	// initialise C with 0s
	vector<int> output;
	for (int i = 0; i < indexN; i++) {
		inputData[scatterIndexVector[i][0]][scatterIndexVector[i][1]] = gatherMatrix [i];
	}
	return inputData;
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
	Result result = read (filename);
    parsec_roi_begin();
	vector< vector< int > > output = scatter(result.inputData, result.scatterIndexVector, result.gatherMatrix);
    parsec_roi_end();
	printMatrix(output);
	return 0;
}
