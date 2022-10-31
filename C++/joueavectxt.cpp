// compile with -std=c++17
#include <iostream>
#include "timeseries.hpp"

#define TYPE double

using namespace std;

int main() {
	size_t n = 1000;
	string path = "../data";
	vector<string> filelist;
	for (const auto& entry : fs::directory_iterator(path))
		filelist.push_back(entry.path());
	size_t nfiles = filelist.size();
	map<size_t, unique_ptr<TimeSeries<TYPE>>> ts;
	for (size_t i = 0; i < nfiles; ++i) {
		ts[i] = make_unique<TimeSeries<TYPE>>(n);
		ts[i]->from_two_column_file(filelist[i]);
		cout << "Moyenne de la serie " << i << " : " << ts[i]->mean() << endl;
	} 
	/* unique_ptr<TimeSeries<TYPE>> a = make_unique<TimeSeries<TYPE>>(n);
	unique_ptr<TimeSeries<TYPE>> b = make_unique<TimeSeries<TYPE>>(n);
	a->from_two_column_file("timeseries1.txt");
	b->from_two_column_file("timeseries2.txt");
	cout << "Moyenne de a : " << a->mean() << endl;
	cout << "Moyenne de b : " << b->mean() << endl;
	cout << "Covariance : " << covariance(a, b) << endl;  */
	return 0;
}
