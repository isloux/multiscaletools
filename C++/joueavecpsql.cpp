// compile with -std=c++17
#include <iostream>
//#include <string>
#include <pqxx/pqxx>
#include <fstream>
#include <vector>
//#include "timeseries.hpp"

using namespace std;

vector<string> credentials(const string& credentialsfile) {
        vector<string> v;
        string v1, v2;
        std::ifstream infile(credentialsfile);
        infile >> v1 >> v2;
        v.push_back(v1);
        v.push_back(v2);
        return v;
}

int main() {
    const auto up = credentials("../../../C++/mini/.credentials");
    string connectionString = "host=localhost dbname=timeseries user=" + up[0] + " password=" + up[1];

    try
    {
        pqxx::connection connectionObject(connectionString.c_str());

        pqxx::work worker(connectionObject);

        pqxx::result response = worker.exec("SELECT * FROM test1");

        for (size_t i = 0; i < response.size(); i++)
        {
            cout << "Id: " << response[i][0] << " Filename: " << response[i][1] << " Number of steps: " << response[i][2] << endl;
        }
    }
    catch (const exception& e)
    {
        cerr << e.what() << endl;
    }

    return 0;
}