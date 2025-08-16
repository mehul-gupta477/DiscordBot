package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"runtime"
	"sync"
	"time"

	_ "github.com/lib/pq"
)

var (
	db     *sql.DB
	mutex  sync.Mutex
	counter int
	globalMap = make(map[string][]byte)
)

// SQL Injection vulnerabilities
func handleLogin(w http.ResponseWriter, r *http.Request) {
	username := r.URL.Query().Get("username")
	password := r.URL.Query().Get("password")
	
	// VULNERABLE: Direct string concatenation - SQL injection risk
	query := "SELECT id FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
	
	rows, err := db.Query(query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()
	
	fmt.Fprintf(w, "Login attempt processed")
}

func searchUsers(w http.ResponseWriter, r *http.Request) {
	searchTerm := r.FormValue("search")
	
	// VULNERABLE: Using fmt.Sprintf for SQL queries
	query := fmt.Sprintf("SELECT * FROM users WHERE name LIKE '%%%s%%'", searchTerm)
	
	rows, err := db.Query(query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()
	
	fmt.Fprintf(w, "Search completed")
}

// Race condition vulnerabilities
func incrementCounter() {
	// VULNERABLE: Unsynchronized access to shared variable
	temp := counter
	time.Sleep(time.Microsecond) // Simulate some processing
	counter = temp + 1
}

func updateGlobalMap(key string, value []byte) {
	// VULNERABLE: Concurrent map access without synchronization
	globalMap[key] = value
}

func racyBankTransfer(fromAccount, toAccount string, amount float64) error {
	// VULNERABLE: Race condition in financial transaction
	var fromBalance, toBalance float64
	
	// Read balances (not atomic)
	err := db.QueryRow("SELECT balance FROM accounts WHERE id = $1", fromAccount).Scan(&fromBalance)
	if err != nil {
		return err
	}
	
	err = db.QueryRow("SELECT balance FROM accounts WHERE id = $1", toAccount).Scan(&toBalance)
	if err != nil {
		return err
	}
	
	// Check and update (race condition window)
	if fromBalance >= amount {
		time.Sleep(time.Millisecond) // Simulate processing delay
		
		// Update balances separately (not atomic)
		_, err = db.Exec("UPDATE accounts SET balance = $1 WHERE id = $2", fromBalance-amount, fromAccount)
		if err != nil {
			return err
		}
		
		_, err = db.Exec("UPDATE accounts SET balance = $1 WHERE id = $2", toBalance+amount, toAccount)
		if err != nil {
			return err
		}
	}
	
	return nil
}

// Database transaction issues
func transferMoney(fromID, toID string, amount float64) error {
	// VULNERABLE: No transaction wrapper - partial updates possible
	_, err := db.Exec("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, fromID)
	if err != nil {
		return err
	}
	
	// If this fails, first update is not rolled back
	_, err = db.Exec("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, toID)
	return err
}

func createUserWithProfile(username, email, profileData string) error {
	// VULNERABLE: Missing transaction - data inconsistency possible
	result, err := db.Exec("INSERT INTO users (username, email) VALUES ($1, $2)", username, email)
	if err != nil {
		return err
	}
	
	userID, _ := result.LastInsertId()
	
	// If this fails, user exists without profile
	_, err = db.Exec("INSERT INTO profiles (user_id, data) VALUES ($1, $2)", userID, profileData)
	return err
}

func updateInventory(productID string, quantity int) error {
	// VULNERABLE: No transaction isolation
	var currentStock int
	err := db.QueryRow("SELECT stock FROM inventory WHERE product_id = $1", productID).Scan(&currentStock)
	if err != nil {
		return err
	}
	
	if currentStock >= quantity {
		// Race condition: stock could change between check and update
		_, err = db.Exec("UPDATE inventory SET stock = stock - $1 WHERE product_id = $2", quantity, productID)
		return err
	}
	
	return fmt.Errorf("insufficient stock")
}

// Memory leak vulnerabilities
func processLargeData() {
	// VULNERABLE: Growing slice without bounds
	var data [][]byte
	
	for i := 0; i < 1000000; i++ {
		// Continuously allocating without cleanup
		chunk := make([]byte, 1024*1024) // 1MB per chunk
		data = append(data, chunk)
		
		// Simulating work but never cleaning up
		if i%1000 == 0 {
			fmt.Printf("Processed %d chunks\n", i)
		}
	}
	// data never gets garbage collected due to scope
}

func leakyGoroutinePool() {
	// VULNERABLE: Goroutines that never terminate
	for i := 0; i < 1000; i++ {
		go func(id int) {
			// Infinite loop without exit condition
			for {
				time.Sleep(time.Second)
				fmt.Printf("Worker %d still running\n", id)
			}
		}(i)
	}
}

func leakyChannelHandler() {
	// VULNERABLE: Channel without proper cleanup
	ch := make(chan []byte, 1000)
	
	go func() {
		for {
			// Continuously sending data but no receiver cleanup
			data := make([]byte, 1024*1024)
			select {
			case ch <- data:
			default:
				// Channel full, but we keep the goroutine alive
				time.Sleep(time.Millisecond)
			}
		}
	}()
	
	// Partial consumption - memory builds up
	for i := 0; i < 10; i++ {
		<-ch
	}
	// Goroutine continues running, channel keeps growing
}

func accumulatingCache() {
	cache := make(map[string][]byte)
	
	// VULNERABLE: Cache that only grows, never cleans up
	for i := 0; i < 1000000; i++ {
		key := fmt.Sprintf("key_%d", i)
		value := make([]byte, 1024) // 1KB per entry
		cache[key] = value
		
		// No expiration or size limits
		if i%10000 == 0 {
			fmt.Printf("Cache size: %d entries\n", len(cache))
		}
	}
}

// Combined vulnerability example
func vulnerableUserRegistration(w http.ResponseWriter, r *http.Request) {
	username := r.FormValue("username")
	email := r.FormValue("email")
	
	// SQL Injection vulnerability
	checkQuery := "SELECT COUNT(*) FROM users WHERE username = '" + username + "'"
	
	var count int
	err := db.QueryRow(checkQuery).Scan(&count)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	
	if count > 0 {
		http.Error(w, "Username already exists", http.StatusBadRequest)
		return
	}
	
	// Race condition: Multiple requests could pass the check
	counter++
	
	// Memory leak: Storing user data indefinitely
	userData := make([]byte, 1024*1024) // 1MB per user
	globalMap[username] = userData
	
	// Transaction issue: No atomicity
	_, err = db.Exec("INSERT INTO users (username, email) VALUES ($1, $2)", username, email)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	
	// This could fail leaving inconsistent state
	_, err = db.Exec("INSERT INTO user_stats (username, login_count) VALUES ($1, 0)", username)
	if err != nil {
		log.Printf("Failed to create user stats: %v", err)
	}
	
	fmt.Fprintf(w, "User registered successfully")
}

func main() {
	// Initialize database connection
	var err error
	db, err = sql.Open("postgres", "postgres://user:pass@localhost/testdb?sslmode=disable")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	
	// Set up HTTP handlers
	http.HandleFunc("/login", handleLogin)
	http.HandleFunc("/search", searchUsers)
	http.HandleFunc("/register", vulnerableUserRegistration)
	
	// Start some vulnerable background processes
	go func() {
		for i := 0; i < 100; i++ {
			go incrementCounter()
			go updateGlobalMap(fmt.Sprintf("key_%d", i), make([]byte, 1024))
		}
	}()
	
	go processLargeData()
	go leakyGoroutinePool()
	go leakyChannelHandler()
	go accumulatingCache()
	
	// Monitor memory usage
	go func() {
		for {
			var m runtime.MemStats
			runtime.ReadMemStats(&m)
			fmt.Printf("Memory usage: %d MB\n", m.Alloc/1024/1024)
			time.Sleep(10 * time.Second)
		}
	}()
	
	fmt.Println("Starting vulnerable server on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}