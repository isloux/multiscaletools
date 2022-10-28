#include <iostream>
#include <vector>
#include <pqxx/pqxx>
#include <fstream>

using std::vector;
using std::string;

typedef struct {
    size_t series_id;
    string filename;
    size_t nsteps;
} timeseries_entry;

class Timeseries_database {
    private:
        string connectionString;

    public:
        Timeseries_database(const string& credentialsfile, const string& dbname) {
            string username, password;
            std::ifstream infile(credentialsfile);
            infile >> username >> password;
            connectionString = "host=localhost dbname=" + dbname + " user=" + username + " password=" + password;
        }

        vector<timeseries_entry> fetch_all_series(const string& tablename) {
            vector<timeseries_entry> v;
            try {
                pqxx::connection connectionObject(connectionString.c_str());
                pqxx::work worker(connectionObject);
                pqxx::result response = worker.exec("SELECT * FROM " + tablename);
                for (const auto row : response)
                    v.push_back({row["series_id"].as<size_t>(), row["filename"].c_str(), row["nsteps"].as<size_t>()});
            }
            catch (const std::exception& e)
            {
                std::cerr << e.what() << std::endl;
            }
            return v;
        }
    
};
