#include <vector>
#include <numeric>
#include <fstream>
#include <filesystem>
#include <assert.h>
#include <functional>
#include <sstream>
#include "database.hpp"

namespace fs = std::filesystem;
using std::vector;

size_t linecounter(const std::string& filename) {
	std::ifstream infile(filename);
    	infile.unsetf(std::ios_base::skipws);
    	return std::count(std::istream_iterator<char>(infile), std::istream_iterator<char>(), '\n');
}

template<typename T>
class TimeSeries {
	private:
		size_t npoints;
		T average;

	public:
		vector<T> t, x;
		
		TimeSeries(const vector<T>& _t, const vector<T>& _x) : t(_t), x(_x), npoints(_t.size()) {}
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
				vector<char> v(content.begin(), content.end());
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
			std::transform(timeseries1->x.begin(), timeseries1->x.end(), tst1.x.begin(), [&](const T _x){ return _x-timeseries1->average; });
			std::transform(timeseries2->x.begin(), timeseries2->x.end(), tst2.x.begin(), [&](const T _x){ return _x-timeseries2->average; });
			std::transform(tst1.x.begin(), tst1.x.end(), tst2.x.begin(), tst1.x.begin(), std::multiplies<T>());		
			T sum = std::accumulate(tst1.x.begin(), tst1.x.end(), static_cast<T>(0));
			return sum/static_cast<T>(timeseries1->x.size());
		}

		template<typename> friend class CovarianceMatrix;
};

template<typename T>
class CovarianceMatrix {
    private:
        const size_t nseries;

    public:
	vector<T> cov;

        CovarianceMatrix(const vector<timeseries_entry>& _timeseries, const size_t& _nsteps) : nseries(_timeseries.size()) {
			using series_id = size_t;
			vector<std::unique_ptr<TimeSeries<T>>> series_vector(nseries);
			{
				series_id i = 0;
				for (auto& series_id_ptr : series_vector) {
					series_id_ptr = std::make_unique<TimeSeries<T>>(_nsteps);
					series_id_ptr->from_binary_file(_timeseries[i].filename);			
					++i;
				}
			}
			for (series_id i = 0; i < nseries; ++i)
				for (series_id j = i; j< nseries; ++j)
					cov.push_back(covariance(series_vector[i], series_vector[j]));
			assert(cov.size() == nseries*(nseries+1)/2);
        }

        ~CovarianceMatrix() {
        	cov.clear();
        }
        
};
