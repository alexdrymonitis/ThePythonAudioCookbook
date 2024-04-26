from countryinfo import CountryInfo
import pycountry as cntry

num_countries = len(cntry.countries)

def exclude_key_error_countries():
	f = open("excluded_countries.txt", "w")
	for i in range(num_countries):
		try:
			CountryInfo(
				list(cntry.countries)[i].name
			).capital()
		except KeyError:
			f.write(str(i)+"\n")
	f.close()

if __name__ == "__main__":
	exclude_key_error_countries()
