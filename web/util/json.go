package util

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

type CatFeeder struct {
	Feed1          FeedJson  `json:"feed1"`
	Feed2          FeedJson  `json:"feed2"`
	Feed3          FeedJson  `json:"feed3"`
	Total          TotalJson `json:"total"`
	DateCalculated string    `json:"date calculated"`
}

type FeedJson struct {
	Amountgiven int  `json:"amountgiven"`
	Deviation   int  `json:"deviation"`
	Wanted      int  `json:"wanted"`
	Time        int  `json:"time"`
	Skip        bool `json:"skip"`
}

type TotalJson struct {
	Deviation   int `json:"deviation"`
	Amountgiven int `json:"amountgiven"`
	Wanted      int `json:"wanted"`
}

func openJson(filename string) []byte {
	// Open our jsonFile
	jsonFile, err := os.Open(filename)
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")
	byteValue, _ := ioutil.ReadAll(jsonFile)
	defer jsonFile.Close()
	return byteValue
}

func LoadJson(jsonfile string) CatFeeder {
	var catFile CatFeeder
	json.Unmarshal(openJson(jsonfile), &catFile)
	return catFile
}

func WriteJson(data CatFeeder, filename string) {

	file, _ := json.MarshalIndent(data, "", " ")
	_ = ioutil.WriteFile(filename, file, 0644)

}
