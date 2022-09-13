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
	vector< vector<int> > indexVector;
};

Result read(string filename) {
	vector< vector<int> > inputData, indexVector;
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
		indexVector.resize(indexVector.size() + 1);
		int a;
		int j = 0;
		while (iss >> a) {
			indexVector[i].push_back(a);
			j++;
		}
		i++;
	}

	infile.close();
	gatherInput.inputData = inputData;
	gatherInput.indexVector = indexVector;
	return gatherInput;
}

vector<int> gather(vector< vector<int> > inputData,
									vector< vector<int> > indexVector) {
	int n = inputData.size();
	int indexN = indexVector.size();
	// initialise C with 0s
	vector<int> output;
	for (int i = 0; i < indexN; i++) {
		output.push_back(inputData[indexVector[i][0]][indexVector[i][1]]);
	}
	return output;
}

void printMatrix(vector<int> matrix) {
	vector<int>::iterator it;
	for (it=matrix.begin(); it != matrix.end(); it++) {
			cout << *it << " ";
		}
		cout << endl;
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
	vector<int> output = gather(result.inputData, result.indexVector);
    parsec_roi_end();
	printMatrix(output);
	return 0;
}
