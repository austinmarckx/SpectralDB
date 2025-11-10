CREATE TABLE Spectra (
    EntryID TEXT NOT NULL,
    Element TEXT,
    Ion INT,
    ObservedWavelengthNanometers FLOAT,
    ObservedWavelengthUncertaintyNanometers FLOAT,
    RelativeIntensity FLOAT,
    EntryReliability TEXT,
    EntryTimestamp TIMESTAMP,
    PRIMARY KEY (EntryID)
);