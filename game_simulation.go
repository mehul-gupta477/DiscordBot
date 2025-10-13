package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Player represents a game player
type Player struct {
	ID        int
	Name      string
	Score     int
	Health    int
	Level     int
	Position  Position
	Inventory []Item
	Attack    int
	Defense   int
	Speed     int
	Gold      int
}

// Position represents a player's position in the game world
type Position struct {
	X, Y int
}

// Item represents an in-game item
type Item struct {
	Name        string
	Type        string // "weapon", "armor", "potion", "treasure"
	Value       int
	Description string
}

// Enemy represents a game enemy
type Enemy struct {
	Name    string
	Health  int
	Attack  int
	Defense int
	Gold    int
	XP      int
}

// Game represents the game state
type Game struct {
	Players    []Player
	Enemies    []Enemy
	Items      []Item
	GameActive bool
	Round      int
	WorldSize  int
	Difficulty string
	TotalGold  int
}

// NewGame creates a new game instance
func NewGame(worldSize int) *Game {
	game := &Game{
		Players:    make([]Player, 0),
		Enemies:    make([]Enemy, 0),
		Items:      make([]Item, 0),
		GameActive: false,
		Round:      0,
		WorldSize:  worldSize,
		Difficulty: "Normal",
		TotalGold:  0,
	}
	game.spawnEnemies()
	game.spawnItems()
	return game
}

// AddPlayer adds a new player to the game
func (g *Game) AddPlayer(name string) {
	player := Player{
		ID:     len(g.Players) + 1,
		Name:   name,
		Score:  0,
		Health: 100,
		Level:  1,
		Position: Position{
			X: rand.Intn(g.WorldSize),
			Y: rand.Intn(g.WorldSize),
		},
		Inventory: make([]Item, 0),
		Attack:    10,
		Defense:   5,
		Speed:     rand.Intn(5) + 5,
		Gold:      100,
	}
	g.Players = append(g.Players, player)
	fmt.Printf("⚔️  Player %s joined the game at position (%d, %d) [ATK:%d DEF:%d SPD:%d]\n",
		player.Name, player.Position.X, player.Position.Y, player.Attack, player.Defense, player.Speed)
}

// StartGame begins the game simulation
func (g *Game) StartGame() {
	if len(g.Players) < 2 {
		fmt.Println("Need at least 2 players to start the game!")
		return
	}

	g.GameActive = true
	g.Round = 1
	fmt.Printf("\n🎮 Game Started with %d players!\n", len(g.Players))
	fmt.Println("=" + string(make([]byte, 40)) + "=")
}

// MovePlayer moves a player to a new random position
func (g *Game) MovePlayer(playerID int) {
	if playerID > len(g.Players) || playerID < 1 {
		return
	}

	player := &g.Players[playerID-1]
	oldPos := player.Position

	// Random movement within bounds
	deltaX := rand.Intn(3) - 1 // -1, 0, or 1
	deltaY := rand.Intn(3) - 1

	newX := player.Position.X + deltaX
	newY := player.Position.Y + deltaY

	// Keep within world bounds
	if newX >= 0 && newX < g.WorldSize {
		player.Position.X = newX
	}
	if newY >= 0 && newY < g.WorldSize {
		player.Position.Y = newY
	}

	fmt.Printf("%s moved from (%d,%d) to (%d,%d)\n",
		player.Name, oldPos.X, oldPos.Y, player.Position.X, player.Position.Y)
}

// SimulateBattle simulates a battle between two nearby players
func (g *Game) SimulateBattle(player1ID, player2ID int) {
	if player1ID > len(g.Players) || player2ID > len(g.Players) ||
		player1ID < 1 || player2ID < 1 || player1ID == player2ID {
		return
	}

	p1 := &g.Players[player1ID-1]
	p2 := &g.Players[player2ID-1]

	// Check if players are close enough to battle (distance <= 2)
	distance := abs(p1.Position.X-p2.Position.X) + abs(p1.Position.Y-p2.Position.Y)
	if distance > 2 {
		return
	}

	fmt.Printf("\n⚔️  Battle between %s and %s!\n", p1.Name, p2.Name)

	// Simple battle simulation
	p1Damage := rand.Intn(20) + 10 + p1.Level*5
	p2Damage := rand.Intn(20) + 10 + p2.Level*5

	p1.Health -= p2Damage
	p2.Health -= p1Damage

	fmt.Printf("%s deals %d damage to %s (Health: %d)\n",
		p1.Name, p1Damage, p2.Name, p2.Health)
	fmt.Printf("%s deals %d damage to %s (Health: %d)\n",
		p2.Name, p2Damage, p1.Name, p1.Health)

	// Determine winner and award points
	if p1.Health <= 0 && p2.Health <= 0 {
		fmt.Println("💀 Both players defeated!")
		p1.Health = 50 // Respawn with half health
		p2.Health = 50
	} else if p1.Health <= 0 {
		fmt.Printf("🏆 %s wins the battle!\n", p2.Name)
		p2.Score += 100
		p1.Health = 50 // Respawn
		g.checkLevelUp(p2)
	} else if p2.Health <= 0 {
		fmt.Printf("🏆 %s wins the battle!\n", p1.Name)
		p1.Score += 100
		p2.Health = 50 // Respawn
		g.checkLevelUp(p1)
	}
	// asdasdfasdas
}

// checkLevelUp checks if a player should level up
func (g *Game) checkLevelUp(player *Player) {
	requiredScore := player.Level * 200
	if player.Score >= requiredScore {
		player.Level++
		player.Health += 20 // Bonus health on level up
		fmt.Printf("🎉 %s leveled up to Level %d!\n", player.Name, player.Level)
	}
}

// SimulateRound simulates one round of the game
func (g *Game) SimulateRound() {
	if !g.GameActive {
		return
	}

	fmt.Printf("\n--- Round %d ---\n", g.Round)

	// Move all players
	for i := range g.Players {
		g.MovePlayer(i + 1)
	}

	// Players encounter enemies
	if len(g.Enemies) > 0 && rand.Intn(100) < 50 {
		playerID := rand.Intn(len(g.Players)) + 1
		aliveEnemies := make([]int, 0)
		for i, enemy := range g.Enemies {
			if enemy.Health > 0 {
				aliveEnemies = append(aliveEnemies, i+1)
			}
		}
		if len(aliveEnemies) > 0 {
			enemyID := aliveEnemies[rand.Intn(len(aliveEnemies))]
			g.PlayerFightEnemy(playerID, enemyID)
		}
	}

	// Players find items
	if len(g.Items) > 0 && rand.Intn(100) < 40 {
		playerID := rand.Intn(len(g.Players)) + 1
		itemID := rand.Intn(len(g.Items)) + 1
		g.PlayerPickupItem(playerID, itemID)
	}

	// Random events
	eventChance := rand.Intn(100)
	if eventChance < 30 {
		g.randomEvent()
	}

	// Check for battles between nearby players
	for i := 0; i < len(g.Players); i++ {
		for j := i + 1; j < len(g.Players); j++ {
			if rand.Intn(100) < 30 { // 30% chance of battle if close
				g.SimulateBattle(i+1, j+1)
			}
		}
	}

	g.Round++
}

// randomEvent triggers a random game event
func (g *Game) randomEvent() {
	events := []string{
		"💰 Treasure found! All players gain 50 points!",
		"🌟 Power-up spawned! Random player gains health!",
		"⚡ Lightning storm! All players lose 10 health!",
		"🍎 Health potions discovered! All players gain 20 health!",
	}

	event := events[rand.Intn(len(events))]
	fmt.Printf("🎲 Random Event: %s\n", event)

	switch event {
	case events[0]: // Treasure
		for i := range g.Players {
			g.Players[i].Score += 50
		}
	case events[1]: // Power-up
		if len(g.Players) > 0 {
			lucky := rand.Intn(len(g.Players))
			g.Players[lucky].Health += 30
			fmt.Printf("   %s received the power-up!\n", g.Players[lucky].Name)
		}
	case events[2]: // Lightning
		for i := range g.Players {
			g.Players[i].Health -= 10
			if g.Players[i].Health < 10 {
				g.Players[i].Health = 10
			}
		}
	case events[3]: // Health potions
		for i := range g.Players {
			g.Players[i].Health += 20
			if g.Players[i].Health > 100 {
				g.Players[i].Health = 100
			}
		}
	}
}

// PrintGameState displays current game state
func (g *Game) PrintGameState() {
	fmt.Println("\n📊 Current Game State:")
	fmt.Println("=" + string(make([]byte, 80)) + "=")

	for _, player := range g.Players {
		fmt.Printf("🎮 %-10s | HP:%-3d | Lvl:%d | Gold:%-4d | ATK:%-2d | DEF:%-2d | Items:%d | Pos:(%d,%d)\n",
			player.Name, player.Health, player.Level, player.Gold, player.Attack,
			player.Defense, len(player.Inventory), player.Position.X, player.Position.Y)
	}

	// Show alive enemies
	aliveEnemies := 0
	for _, enemy := range g.Enemies {
		if enemy.Health > 0 {
			aliveEnemies++
		}
	}
	fmt.Printf("\n👹 Enemies Remaining: %d/%d | 💎 Items Available: %d | 💰 Total Gold Earned: %d\n",
		aliveEnemies, len(g.Enemies), len(g.Items), g.TotalGold)
	fmt.Println()
}

// GetWinner returns the player with the highest score
func (g *Game) GetWinner() *Player {
	if len(g.Players) == 0 {
		return nil
	}

	winner := &g.Players[0]
	for i := range g.Players {
		if g.Players[i].Score > winner.Score {
			winner = &g.Players[i]
		}
	}
	return winner
}

// EndGame ends the game and declares winner
func (g *Game) EndGame() {
	g.GameActive = false
	winner := g.GetWinner()

	fmt.Println("\n🏁 Game Over!")
	fmt.Println("=" + string(make([]byte, 40)) + "=")

	if winner != nil {
		fmt.Printf("🥇 Winner: %s with %d points!\n", winner.Name, winner.Score)
	}

	fmt.Println("\nFinal Standings:")
	// Sort players by score (simple bubble sort for demo)
	players := make([]Player, len(g.Players))
	copy(players, g.Players)

	for i := 0; i < len(players); i++ {
		for j := 0; j < len(players)-1-i; j++ {
			if players[j].Score < players[j+1].Score {
				players[j], players[j+1] = players[j+1], players[j]
			}
		}
	}

	for i, player := range players {
		fmt.Printf("%d. %s - %d points (Level %d)\n",
			i+1, player.Name, player.Score, player.Level)
	}
}

// abs returns absolute value of an integer
func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// spawnEnemies spawns enemies in the game world
func (g *Game) spawnEnemies() {
	enemyTypes := []struct {
		Name    string
		Health  int
		Attack  int
		Defense int
		Gold    int
		XP      int
	}{
		{"Goblin", 30, 8, 3, 20, 50},
		{"Orc", 50, 12, 5, 35, 75},
		{"Troll", 70, 15, 8, 50, 100},
		{"Dragon", 150, 25, 15, 200, 300},
		{"Skeleton", 25, 7, 2, 15, 40},
	}

	numEnemies := rand.Intn(5) + 3 // 3-7 enemies
	for i := 0; i < numEnemies; i++ {
		enemyType := enemyTypes[rand.Intn(len(enemyTypes))]
		enemy := Enemy{
			Name:    fmt.Sprintf("%s_%d", enemyType.Name, i+1),
			Health:  enemyType.Health,
			Attack:  enemyType.Attack,
			Defense: enemyType.Defense,
			Gold:    enemyType.Gold,
			XP:      enemyType.XP,
		}
		g.Enemies = append(g.Enemies, enemy)
	}
	fmt.Printf("👹 Spawned %d enemies in the world!\n", numEnemies)
}

// spawnItems spawns items in the game world
func (g *Game) spawnItems() {
	itemTemplates := []Item{
		{"Iron Sword", "weapon", 15, "A sturdy iron sword"},
		{"Steel Shield", "armor", 12, "Provides good protection"},
		{"Health Potion", "potion", 25, "Restores 25 HP"},
		{"Golden Coin", "treasure", 50, "Worth 50 gold"},
		{"Magic Amulet", "treasure", 100, "A valuable magical item"},
		{"Diamond Ring", "treasure", 150, "A precious diamond ring"},
		{"Battle Axe", "weapon", 20, "Deals massive damage"},
		{"Leather Armor", "armor", 8, "Basic protection"},
	}

	numItems := rand.Intn(8) + 5 // 5-12 items
	for i := 0; i < numItems; i++ {
		item := itemTemplates[rand.Intn(len(itemTemplates))]
		g.Items = append(g.Items, item)
	}
	fmt.Printf("💎 Spawned %d items in the world!\n", numItems)
}

// PlayerFightEnemy makes a player fight an enemy
func (g *Game) PlayerFightEnemy(playerID int, enemyID int) {
	if playerID > len(g.Players) || playerID < 1 || enemyID > len(g.Enemies) || enemyID < 1 {
		return
	}

	player := &g.Players[playerID-1]
	enemy := &g.Enemies[enemyID-1]

	if enemy.Health <= 0 {
		return // Enemy already defeated
	}

	fmt.Printf("\n⚔️  %s encounters %s!\n", player.Name, enemy.Name)

	// Calculate damage
	playerDamage := player.Attack + rand.Intn(10) - enemy.Defense
	if playerDamage < 1 {
		playerDamage = 1
	}

	enemyDamage := enemy.Attack + rand.Intn(8) - player.Defense
	if enemyDamage < 1 {
		enemyDamage = 1
	}

	// Apply damage
	enemy.Health -= playerDamage
	player.Health -= enemyDamage

	fmt.Printf("  %s deals %d damage to %s (Enemy HP: %d)\n",
		player.Name, playerDamage, enemy.Name, max(0, enemy.Health))
	fmt.Printf("  %s deals %d damage to %s (Player HP: %d)\n",
		enemy.Name, enemyDamage, player.Name, max(0, player.Health))

	// Check for victory
	if enemy.Health <= 0 {
		player.Gold += enemy.Gold
		player.Score += enemy.XP
		g.TotalGold += enemy.Gold
		fmt.Printf("  🏆 %s defeated %s! Gained %d gold and %d XP!\n",
			player.Name, enemy.Name, enemy.Gold, enemy.XP)
		g.checkLevelUp(player)
	}

	if player.Health <= 0 {
		player.Health = 50                   // Respawn
		player.Gold = max(0, player.Gold-20) // Lose some gold
		fmt.Printf("  💀 %s was defeated! Respawned with 50 HP (Lost 20 gold)\n", player.Name)
	}
}

// PlayerPickupItem makes a player pick up an item
func (g *Game) PlayerPickupItem(playerID int, itemID int) {
	if playerID > len(g.Players) || playerID < 1 || itemID > len(g.Items) || itemID < 1 {
		return
	}

	player := &g.Players[playerID-1]
	item := g.Items[itemID-1]

	player.Inventory = append(player.Inventory, item)
	fmt.Printf("💰 %s picked up %s!\n", player.Name, item.Name)

	// Apply item effects
	switch item.Type {
	case "weapon":
		player.Attack += item.Value
		fmt.Printf("  ⚔️  Attack increased by %d!\n", item.Value)
	case "armor":
		player.Defense += item.Value
		fmt.Printf("  🛡️  Defense increased by %d!\n", item.Value)
	case "potion":
		player.Health += item.Value
		if player.Health > 100 {
			player.Health = 100
		}
		fmt.Printf("  ❤️  Health restored by %d!\n", item.Value)
	case "treasure":
		player.Gold += item.Value
		player.Score += item.Value
		fmt.Printf("  💰 Gained %d gold!\n", item.Value)
	}

	// Remove item from world
	g.Items = append(g.Items[:itemID-1], g.Items[itemID:]...)
}

// max returns the maximum of two integers
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// UsePotion allows a player to use a potion from inventory
func (g *Game) UsePotion(playerID int) {
	if playerID > len(g.Players) || playerID < 1 {
		return
	}

	player := &g.Players[playerID-1]

	// Find potion in inventory
	for i, item := range player.Inventory {
		if item.Type == "potion" {
			player.Health += item.Value
			if player.Health > 100 {
				player.Health = 100
			}
			fmt.Printf("💊 %s used %s! HP restored to %d\n",
				player.Name, item.Name, player.Health)
			// Remove used potion
			player.Inventory = append(player.Inventory[:i], player.Inventory[i+1:]...)
			return
		}
	}
}

// Main function to run the game simulation
func main() {
	rand.Seed(time.Now().UnixNano())

	fmt.Println("🎮 Welcome to the Discord Bot Game Simulation!")
	fmt.Println("=" + string(make([]byte, 45)) + "=")

	// Create new game
	game := NewGame(10) // 10x10 world

	// Add players
	playerNames := []string{"Alice", "Bob", "Charlie", "Diana", "Eve"}
	for _, name := range playerNames {
		game.AddPlayer(name)
	}

	// Start the game
	game.StartGame()

	// Simulate 10 rounds
	for round := 1; round <= 10; round++ {
		game.SimulateRound()
		game.PrintGameState()

		// Add some delay for readability
		time.Sleep(500 * time.Millisecond)
	}

	// End the game dasdasdas
	game.EndGame()
}
