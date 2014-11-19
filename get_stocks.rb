require 'date'
require 'open-uri'

# usage ruby get_stocks.rb #{STOCK_SYMBOLS} #{NUMBER_OF_YEARS}

unless ARGV.length == 2
  puts "Incorrect Usage. Use: ruby get_stocks.rb {STOCK_SYMBOLS_FILE} {NUMBER_OF_YEARS}"
else
  current_date = Date.parse(Time.now.to_s)
  filename = ARGV[0]
  num_years = ARGV[1].to_i
  directory = "#{current_date.to_s}_#{num_years}yr"
  symbols = []

  # remove existing directory
  system("rm -rf #{directory}")
  system("mkdir #{directory}")

  # read stock symbols from file
  File.foreach(filename) do |sym|
    sym.chomp!
    puts "Fetching #{sym}..."
    # api url for stock data retrieval
    retrieval_url = "http://real-chart.finance.yahoo.com/table.csv?s=#{sym}" +
      "&a=#{current_date.month - 1}&b=#{current_date.day}&c=#{current_date.year - num_years}&d=#{current_date.month - 1}" +
      "&e=#{current_date.day}&f=#{current_date.year}&g=d&ignore=.csv"
    begin
      open("#{directory}/#{sym}.csv", "wb") do |file|
        file << open(retrieval_url).read
      end
      symbols << sym
    rescue
      puts "Unable to retrieve #{sym}"
    end
  end

  File.open("#{directory}/symbol_list.txt", "wb") do |file|
    symbols.each { |sym| file.puts sym }
  end

  puts "DONE"
end