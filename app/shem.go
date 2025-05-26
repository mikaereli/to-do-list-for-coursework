package scheme

import (
	"net/http"
	"strconv"
	"time"
)

type Task struct {
	number       int
	title        string
	descrip      string
	data_created time.Time
}

func NewTask(number int, title string, descrip string) Task {
	return Task{
		number:       number,
		title:        title,
		descrip:      descrip,
		data_created: time.Now(),
	}
}

func (t Task) GetNumber() int {
	return t.number
}

func getNumber(w http.ResponseWriter, r *http.Request) int {
	number := r.URL.Query().Get("number")
	if number == "" {
		http.Error(w, "number is required", http.StatusBadRequest)
		return 0
	}
	num, err := strconv.Atoi(number)
	if err != nil {
		http.Error(w, "number must be an integer", http.StatusBadRequest)
		return 0
	}
	return num
}
