package main

import (
	"log"
	"net/http"

	svg "github.com/ajstarks/svgo"
)

func main() {
	http.Handle("/circle", http.HandlerFunc(circle))
	http.Handle("/cards", http.HandlerFunc(cards))
	err := http.ListenAndServe(":2003", nil)
	if err != nil {
		log.Fatal("ListenAndServe:", err)
	}
}

func cards(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "image/svg+xml")
	s := svg.New(w)
	scale := 5
	width := 210 * scale
	height := 297 * scale

	cardsH := 4
	cardsV := 4

	cardW := (width - 10) / cardsH
	cardH := (height - 10) / cardsV

	s.Start(width, height)
	s.Rect(0, 0, width, height, "fill:pink")
	for x := 0; x < cardsH; x++ {
		for y := 0; y < cardsV; y++ {
			s.Roundrect(5+x*cardW, 5+y*cardH, cardW, cardH, 5*scale, 5*scale, "fill:white;stroke:black;stroke-width:5")
		}

	}
	s.End()
}

func circle(w http.ResponseWriter, req *http.Request) {
	w.Header().Set("Content-Type", "image/svg+xml")
	s := svg.New(w)
	s.Start(500, 500)
	s.Circle(250, 250, 125, "fill:none;stroke:black")
	s.End()
}
