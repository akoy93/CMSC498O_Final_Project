require 'date'
require 'open-uri'

# usage ruby get_stocks.rb #{STOCK_SYMBOLS} #{NUMBER_OF_BARS}

unless ARGV.length == 2
  puts "Incorrect Usage. Use: ruby get_stocks.rb {STOCK_SYMBOLS_FILE} {NUMBER_OF_BARS}"
else
  current_date = Date.parse(Time.now.to_s)
  filename = ARGV[0]
  num_bars = ARGV[1].to_i
  directory = "#{current_date.to_s}_#{num_bars}"
  symbols = []

  # remove existing directory
  system("rm -rf #{directory}")
  system("mkdir #{directory}")

  # read stock symbols from file
  File.foreach(filename) do |sym|
    sym.chomp!
    puts "Fetching #{sym}..."
    # api url for stock data retrieval
    start_date = current_date - num_bars
    retrieval_url = "http://real-chart.finance.yahoo.com/table.csv?s=#{sym}" +
      "&a=#{start_date.month - 1}&b=#{start_date.day}&c=#{start_date.year}&d=#{current_date.month - 1}" +
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