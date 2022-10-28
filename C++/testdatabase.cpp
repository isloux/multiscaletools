// compile with -lpqxx

#include "timeseries.hpp"

using namespace std;

int main() {
    string dbname = "timeseries";
    unique_ptr<Timeseries_database> labase = make_unique<Timeseries_database>("../../../C++/mini/.credentials", dbname);
    const auto series_vector = labase->fetch_all_series("test1");
    for (const auto& x : series_vector)
        cout << x.series_id << ' ' << x.filename << ' ' << x.nsteps << endl;
    // Need to check that all nsteps are the same
    //unique_ptr<CovarianceMatrix<double>> covariance_matrix = make_unique<CovarianceMatrix<double>>(series_vector, series_vector[0].nsteps);
    return 0;
}