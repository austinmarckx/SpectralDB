# DB:
## TODO:

1) Create SQL Table to hold cleaned elements
2) Insert all cleaned elements into SQL table
3) Search functionalities for Table

## Notes

[x] load_element
- Loads the raw data files retrieved from ASD database
[x] preprocess
- preprocess raw data file:
    - trimmed: Subset, rename columns; drop missing vals; convert types; and add custom features
    - xyz: Convert wavelength into CIE_XYZ representation

## Examples:
> Zn = load_element("Zn")
> Pb = load_element("Lead")
> He = preprocess("He")
> Y_trim = preprocess("Yttrium", trimmed=True)
> Ag_trim_xyz = preprocess("Yttrium", trimmed=True, xyz=True)


# Model:
## TODO:

1) Make Reference matrix better defined (not just one function from one guy)

## Notes

[x] WSS wavelength to XYZ:
- Currently have:
    - simple degree 2
    - simple degree 10
    - multi degree 2

Test cases relatively thorough for WSS (at least for running)
- I really am not sure what datapoints I could use to analytically validate the results.

## Examples:
> WSS.fit(421)
> WSS.fit(421,"single")
> WSS.fit(421, how="single", deg="10")

# Viz:
## TODO:

[x] spectral density plot
[x] spectral band plot
- Default colorscale makes z-value log10(intensity) reported in raw data
- if set to `reference`, colorscale replaced with actual RGB color corresponding to wavelength

## Examples:

> spectral_density(["Zinc", "Argon", "Uranium"])
> visible_spectral_density("Uranium", bin_size=10)
> heatmap( ("Zn", "Ar", "H") )
> heatmap(("Zn", "Ar", "H"), colorscale="reference", maxval=730)
> reference_heatmap("Cu")
> reference_heatmap(["H", "Li", "Na", "K", "Rb", "Cs", "Fr"], maxval=680)


## Notes

Play around with and figure out how to represent the spectral lines as images

--> element(s) to colormap

https://engineering.purdue.edu/~bouman/ece637/notes/pdf/Tristimulus.pdf
    • CIE 1931 Standard 2
– R, G, B color primaries are defined by pure line spectra (delta functions in wavelength) at 700nm, 546.1nm,
and 435.8nm.

let's start with D65 whitepoint. or illuminant E
https://www.color.org/chardata/colorimetry/index.xalter

http://www.cvrl.org/database/text/intros/introcmfs.htm

O_O
https://en.wikipedia.org/wiki/Standard_illuminant#Illuminant_E
https://en.wikipedia.org/wiki/CIE_1931_color_space#Tristimulus_values
https://en.wikipedia.org/wiki/RGB_color_spaces
