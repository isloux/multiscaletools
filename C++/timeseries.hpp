#include <vector>
#include <numeric>
#include <fstream>
#include <filesystem>
#include <assert.h>
#include <functional>
#include <sstream>

namespace fs = std::filesystem;

template<typename T>
class TimeSeries {
	private:
		size_t npoints;
		T average;

	public:
		std::vector<T> t, x;
		
		TimeSeries(const std::vector<T>& _t, const std::vector<T>& _x) : t(_t), x(_x), npoints(_t.size()) {}
		TimeSeries(const size_t& _n) : npoints(_n) {
			/* t.reserve(_n);
			x.reserve(_n); */
		}
		
		~TimeSeries() {
			t.clear();
			x.clear();
		}
		
		T mean() {
			if (x.size() > 0) {
				T sum = std::accumulate(x.begin(), x.end(), static_cast<T>(0));
				average = sum/static_cast<T>(x.size());
				return average;
			} else {
				return 0;
			}
		}
		
		void from_two_column_file(const std::string& filename) {
			if (fs::exists(filename)) {
				std::ifstream infile(filename);
				T v1, v2;
				for (size_t i = 0; i < npoints; ++i) {
					infile >> v1 >> v2;
					t.push_back(v1);
					x.push_back(v2);
				}
			}	
		}

		void from_binary_file(const std::string& filename) {
			if (fs::exists(filename)) {
				std::ifstream infile(filename);
                auto ss = std::ostringstream();
				ss << infile.rdbuf();
				std::string content = ss.str();
				std::vector<char> v(content.begin(), content.end());
				assert (sizeof(double) == 8);
				size_t nchar = 8;
				size_t nstring = v.size()/nchar;
				size_t k = 0;
				union { char b[8]; double d; };
				for (size_t i = 0; i < nstring; ++i) {
					for (size_t j = 0; j < nchar; ++j) {
						b[j] = v[k];
						++k;
					}
					x.push_back(d);
        		}
			}
		}

		friend T covariance(const std::unique_ptr<TimeSeries<T>>& timeseries1, const std::unique_ptr<TimeSeries<T>>& timeseries2) {
			assert(timeseries1->x.size() == timeseries2->x.size());
			TimeSeries<T> tst1 = *timeseries1;
			TimeSeries<T> tst2 = *timeseries2;
			std::transform(timeseries1->x.begin(), timeseries1->x.end(), tst1.x.begin(), [&](T _x){ return _x-timeseries1->average; });
			std::transform(timeseries2->x.begin(), timeseries2->x.end(), tst2.x.begin(), [&](T _x){ return _x-timeseries2->average; });
			std::transform(tst1.x.begin(), tst1.x.end(), tst2.x.begin(), tst1.x.begin(), std::multiplies<T>());		
			T sum = std::accumulate(tst1.x.begin(), tst1.x.end(), static_cast<T>(0));
			return sum/static_cast<T>(timeseries1->x.size());
		}
};
