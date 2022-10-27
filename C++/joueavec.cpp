// compile with -std=c++17
#include <iostream>
#include "timeseries.hpp"

#define TYPE double

using namespace std;

int main() {
	size_t n = 1000;
	unique_ptr<TimeSeries<TYPE>> a = make_unique<TimeSeries<TYPE>>(n);
	unique_ptr<TimeSeries<TYPE>> b = make_unique<TimeSeries<TYPE>>(n);
	a->from_column_file("timeseries1.txt");
	b->from_column_file("timeseries2.txt");
	cout << "Moyenne de a : " << a->mean() << endl;
	cout << "Moyenne de b : " << b->mean() << endl;
	cout << "Covariance : " << covariance(a, b) << endl;
	return 0;
}
