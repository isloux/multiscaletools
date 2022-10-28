// compile with -lpqxx

#include "database.hpp"

using namespace std;

int main() {
    string dbname = "timeseries";
    unique_ptr<Timeseries_database> labase = make_unique<Timeseries_database>("../../../C++/mini/.credentials", dbname);
    const auto series_vector = labase->fetch_all_series("test1");
    for (const auto& x : series_vector)
        std::cout << x.series_id << ' ' << x.filename << ' ' << x.nsteps << endl;
    return 0;
}