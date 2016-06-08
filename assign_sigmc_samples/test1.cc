#include <iostream>
#include <fstream>
#include <vector>
#include <random>

#include <PsqlReader.h>
#include <CsvWriter.h>
#include <pgstring_utils.h>

#include <boost/program_options.hpp>

namespace po = boost::program_options;
namespace pu = pgstring_utils;

// sample index mapping:
// explore => 1, train => 2, validate => 3, test => 4, unassigned => 0
//
// assign samples in the following proportion
// explore : train : validate : test : unassigned = 1 : 0.5 : 0.5 : 1 : 2
int assign_sample(double r) {
  if (r < 0.2) { return 1; }
  if (r < 0.3) { return 2; }
  if (r < 0.4) { return 3; }
  if (r < 0.6) { return 4; }
  return 0;
}

int main() {

  // open output csv file
  CsvWriter csv;
  csv.open("sigmc_sample_assignments.csv", {
      "eid", "sample_type"
  });

  // open database connection and populate fields
  PsqlReader psql;
  psql.open_connection("dbname=testing");
  psql.open_cursor(
      "framework_ntuples_sigmc", 
      { "eid" });

  // random real generator. fixed seed for reproducibility.
  std::mt19937 gen; gen.seed(1);
  std::uniform_real_distribution<> dis(0, 1);

  // main loop to extract information 
  int eid; 
  while (psql.next()) {

    pu::string2type(psql.get("eid"), eid);
    csv.set("eid", pu::type2string(eid));
    csv.set("sample_type", pu::type2string(assign_sample(dis(gen))));

    csv.commit();
  }

  // close database connection
  psql.close_cursor();
  psql.close_connection();

  // close output file
  csv.close();

  return 0;
}

