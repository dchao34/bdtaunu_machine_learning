#include <iostream>
#include <fstream>
#include <vector>

#include <PsqlReader.h>
#include <CsvWriter.h>
#include <pgstring_utils.h>

#include <boost/program_options.hpp>

namespace po = boost::program_options;
namespace pu = pgstring_utils;

void assign_candidate_selection_mclabels(const po::variables_map &vm);

int main(int argc, char **argv) {

  try {

    // define program options
    po::options_description generic("Generic options");
    generic.add_options()
        ("help,h", "produce help message")
    ;

    po::options_description config("Configuration options");
    config.add_options()
        ("dbname", po::value<std::string>(), 
             "database name. ")
        ("table_name", po::value<std::string>(), 
             "name of the truth match table. ")
        ("output_fname", po::value<std::string>(), 
             "output csv file name. ")
        ("cursor_fetch_size", po::value<int>()->default_value(5000), 
             "number of rows per cursor fetch. ")
    ;

    po::options_description hidden("Hidden options");
    hidden.add_options()
        ("config_file", po::value<std::string>(), 
             "name of a configuration file. ")
    ;

    po::options_description cmdline_options;
    cmdline_options.add(generic).add(config).add(hidden);

    po::options_description config_file_options;
    config_file_options.add(config);

    po::options_description visible;
    visible.add(generic).add(config);

    po::positional_options_description p;
    p.add("config_file", -1);

    // parse program options and configuration file
    po::variables_map vm;
    store(po::command_line_parser(argc, argv).
          options(cmdline_options).positional(p).run(), vm);
    notify(vm);

    if (vm.count("help") || !vm.count("config_file")) {
      std::cout << std::endl;
      std::cout << "Usage: ./assign_candidate_selection_mclabels ";
      std::cout << "[options] config_fname" << std::endl;
      std::cout << visible << "\n";
      return 0;
    }

    std::ifstream fin(vm["config_file"].as<std::string>());
    if (!fin) {
      std::cout << "cannot open config file: ";
      std::cout << vm["config_file"].as<std::string>() << std::endl;
      return 0;
    }

    store(parse_config_file(fin, config_file_options), vm);
    notify(vm);

    // main routine
    assign_candidate_selection_mclabels(vm);

  } catch(std::exception& e) {

    std::cerr << "error: " << e.what() << "\n";
    return 1;

  } catch(...) {

    std::cerr << "Exception of unknown type!\n";
    return 1;
  }

  return 0;
}


void assign_candidate_selection_mclabels(const po::variables_map &vm) {

  // open database connection and populate fields
  std::string dbname = vm["dbname"].as<std::string>();
  std::string table_name = vm["table_name"].as<std::string>();
  int cursor_fetch_size = vm["cursor_fetch_size"].as<int>();

  // open database connection and populate fields
  PsqlReader psql;
  psql.open_connection("dbname="+dbname);
  psql.open_cursor(table_name, 
      { "eid", "y_match_status" }, cursor_fetch_size);

  // open output csv file
  std::string output_fname = vm["output_fname"].as<std::string>();
  CsvWriter csv;
  csv.open(output_fname, {
      "eid", "cidx", "is_matched"
  });

  // main loop to extract information 
  int eid; 
  std::vector<int> y_match_status;
  while (psql.next()) {

    pu::string2type(psql.get("eid"), eid);
    pu::string2type(psql.get("y_match_status"), y_match_status);

    for (size_t i = 0; i < y_match_status.size(); ++i) {
      csv.set("eid", pu::type2string(eid));
      csv.set("cidx", pu::type2string(i));
      csv.set("is_matched", pu::type2string(y_match_status[i]));
      csv.commit();
    }
  }

  // close database connection
  psql.close_cursor();
  psql.close_connection();

  // close output file
  csv.close();

}

