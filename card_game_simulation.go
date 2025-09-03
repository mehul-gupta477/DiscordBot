package main

import (
	"fmt"
	"math/rand"
	"sort"
	"time"
)

// Card represents a playing card dasdasdasadsdas
type Card struct {
	Suit  string
	Rank  string
	Value int
}

// Deck represents a deck of cards dsdasdas
type Deck struct {
	Cards []Card
}

// CardPlayer represents a player in the card game dada 1234
type CardPlayer struct {
	ID       int
	Name     string
	Hand     []Card
	Score    int
	Wins     int
	IsActive bool
}

// CardGame represents the card game states123
type CardGame struct {
	Players     []CardPlayer
	Deck        Deck
	CurrentTurn int
	Round       int
	GameActive  bool
	GameType    string
	DiscardPile []Card
}

// NewCardGame creates a new card game instances
func NewCardGame(gameType string) *CardGame {
	return &CardGame{
		Players:     make([]CardPlayer, 0),
		Deck:        NewStandardDeck(),
		CurrentTurn: 0,
		Round:       1,
		GameActive:  false,
		GameType:    gameType,
		DiscardPile: make([]Card, 0),
	}
}

// NewStandardDeck creates a standard 52-card deck
func NewStandardDeck() Deck {
	suits := []string{"♠️", "♥️", "♦️", "♣️"}
	ranks := []string{"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
	values := []int{14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}

	var cards []Card
	for _, suit := range suits {
		for i, rank := range ranks {
			card := Card{
				Suit:  suit,
				Rank:  rank,
				Value: values[i],
			}
			cards = append(cards, card)
		}
	}

	return Deck{Cards: cards}
}

// Shuffle shuffles the deck
func (d *Deck) Shuffle() {
	for i := len(d.Cards) - 1; i > 0; i-- {
		j := rand.Intn(i + 1)
		d.Cards[i], d.Cards[j] = d.Cards[j], d.Cards[i]
	}
}

// DrawCard draws a card from the top of the deck
func (d *Deck) DrawCard() (Card, bool) {
	if len(d.Cards) == 0 {
		return Card{}, false
	}

	card := d.Cards[0]
	d.Cards = d.Cards[1:]
	return card, true
}

// AddCard adds a card to the bottom of the deck
func (d *Deck) AddCard(card Card) {
	d.Cards = append(d.Cards, card)
}

// String returns string representation of a card
func (c Card) String() string {
	return fmt.Sprintf("%s%s", c.Rank, c.Suit)
}

// AddPlayer adds a new player to the card game
func (g *CardGame) AddPlayer(name string) {
	player := CardPlayer{
		ID:       len(g.Players) + 1,
		Name:     name,
		Hand:     make([]Card, 0),
		Score:    0,
		Wins:     0,
		IsActive: true,
	}
	g.Players = append(g.Players, player)
	fmt.Printf("🎴 Player %s joined the %s game!\n", player.Name, g.GameType)
}

// StartGame begins the card game
func (g *CardGame) StartGame() {
	if len(g.Players) < 2 {
		fmt.Println("Need at least 2 players to start the card game!")
		return
	}

	g.GameActive = true
	g.Deck.Shuffle()

	fmt.Printf("\n🃏 %s Game Started with %d players!\n", g.GameType, len(g.Players))
	fmt.Println("=" + string(make([]rune, 50, 50)) + "=")

	// Deal initial cards based on game type
	switch g.GameType {
	case "BlackJack":
		g.dealBlackJackCards()
	case "Poker":
		g.dealPokerCards()
	case "HighCard":
		g.dealHighCardGame()
	default:
		g.dealHighCardGame()
	}
}

// dealBlackJackCards deals 2 cards to each player for BlackJack
func (g *CardGame) dealBlackJackCards() {
	for i := 0; i < 2; i++ {
		for j := range g.Players {
			if card, ok := g.Deck.DrawCard(); ok {
				g.Players[j].Hand = append(g.Players[j].Hand, card)
			}
		}
	}
	fmt.Println("🃏 Dealt 2 cards to each player for BlackJack!")
}

// dealPokerCards deals 5 cards to each player for Poker
func (g *CardGame) dealPokerCards() {
	for i := 0; i < 5; i++ {
		for j := range g.Players {
			if card, ok := g.Deck.DrawCard(); ok {
				g.Players[j].Hand = append(g.Players[j].Hand, card)
			}
		}
	}
	fmt.Println("🃏 Dealt 5 cards to each player for Poker!")
}

// dealHighCardGame deals 1 card to each player
func (g *CardGame) dealHighCardGame() {
	for j := range g.Players {
		if card, ok := g.Deck.DrawCard(); ok {
			g.Players[j].Hand = append(g.Players[j].Hand, card)
		}
	}
	fmt.Println("🃏 Dealt 1 card to each player for High Card!")
}

// PlayRound plays one round of the game
func (g *CardGame) PlayRound() {
	if !g.GameActive {
		return
	}

	fmt.Printf("\n--- Round %d ---\n", g.Round)

	switch g.GameType {
	case "BlackJack":
		g.playBlackJackRound()
	case "Poker":
		g.playPokerRound()
	case "HighCard":
		g.playHighCardRound()
	default:
		g.playHighCardRound()
	}

	g.Round++
}

// playBlackJackRound plays a BlackJack round
func (g *CardGame) playBlackJackRound() {
	fmt.Println("🎯 BlackJack Round!")

	for i := range g.Players {
		player := &g.Players[i]
		if !player.IsActive {
			continue
		}

		handValue := g.calculateBlackJackValue(player.Hand)
		fmt.Printf("%s's hand value: %d ", player.Name, handValue)
		g.printHand(player.Hand)

		// Simple AI: Hit if under 17
		if handValue < 17 && len(g.Deck.Cards) > 0 {
			if card, ok := g.Deck.DrawCard(); ok {
				player.Hand = append(player.Hand, card)
				newValue := g.calculateBlackJackValue(player.Hand)
				fmt.Printf("  %s hits! Drew %s. New value: %d\n", player.Name, card, newValue)

				if newValue > 21 {
					fmt.Printf("  💥 %s busts with %d!\n", player.Name, newValue)
					player.IsActive = false
				}
			}
		} else {
			fmt.Printf("  %s stands with %d\n", player.Name, handValue)
		}
	}

	// Check for round winner
	g.determineBlackJackWinner()
}

// calculateBlackJackValue calculates BlackJack hand value
func (g *CardGame) calculateBlackJackValue(hand []Card) int {
	value := 0
	aces := 0

	for _, card := range hand {
		if card.Rank == "A" {
			aces++
			value += 11
		} else if card.Rank == "J" || card.Rank == "Q" || card.Rank == "K" {
			value += 10
		} else {
			value += card.Value
		}
	}

	// Adjust for aces
	for aces > 0 && value > 21 {
		value -= 10
		aces--
	}

	return value
}

// determineBlackJackWinner determines the winner of BlackJack round
func (g *CardGame) determineBlackJackWinner() {
	bestValue := 0
	var winners []int

	for i, player := range g.Players {
		if !player.IsActive {
			continue
		}

		handValue := g.calculateBlackJackValue(player.Hand)
		if handValue <= 21 {
			if handValue > bestValue {
				bestValue = handValue
				winners = []int{i}
			} else if handValue == bestValue {
				winners = append(winners, i)
			}
		}
	}

	if len(winners) == 1 {
		winner := &g.Players[winners[0]]
		winner.Score += 100
		winner.Wins++
		fmt.Printf("🏆 %s wins the BlackJack round with %d!\n", winner.Name, bestValue)
	} else if len(winners) > 1 {
		fmt.Printf("🤝 Tie between %d players with %d!\n", len(winners), bestValue)
		for _, winnerIdx := range winners {
			g.Players[winnerIdx].Score += 50
		}
	} else {
		fmt.Println("💥 All players busted!")
	}
}

// playPokerRound plays a Poker round
func (g *CardGame) playPokerRound() {
	fmt.Println("🃏 Poker Round!")

	for i := range g.Players {
		player := &g.Players[i]
		handRank := g.evaluatePokerHand(player.Hand)
		fmt.Printf("%s's hand rank: %d ", player.Name, handRank)
		g.printHand(player.Hand)
		player.Score = handRank // Use hand rank as score for poker
	}

	g.determinePokerWinner()
}

// evaluatePokerHand evaluates poker hand (simplified)
func (g *CardGame) evaluatePokerHand(hand []Card) int {
	if len(hand) != 5 {
		return 0
	}

	// Sort hand by value
	sortedHand := make([]Card, len(hand))
	copy(sortedHand, hand)
	sort.Slice(sortedHand, func(i, j int) bool {
		return sortedHand[i].Value < sortedHand[j].Value
	})

	// Check for pairs, three of a kind, etc. (simplified)
	values := make(map[int]int)
	suits := make(map[string]int)

	for _, card := range sortedHand {
		values[card.Value]++
		suits[card.Suit]++
	}

	// Check for flush
	isFlush := len(suits) == 1

	// Check for straight
	isStraight := true
	for i := 1; i < len(sortedHand); i++ {
		if sortedHand[i].Value != sortedHand[i-1].Value+1 {
			isStraight = false
			break
		}
	}
	
	// Check for Ace-low straight (A-2-3-4-5)
	if !isStraight && len(sortedHand) == 5 {
		if sortedHand[0].Value == 1 && sortedHand[1].Value == 2 && 
		   sortedHand[2].Value == 3 && sortedHand[3].Value == 4 && 
		   sortedHand[4].Value == 5 {
			isStraight = true
		}
	}

	// Determine hand rank (higher is better)
	if isFlush && isStraight {
		return 8 // Straight flush
	} else if g.hasOfAKind(values, 4) {
		return 7 // Four of a kind
	} else if g.hasOfAKind(values, 3) && g.hasOfAKind(values, 2) && len(values) == 2 {  
        return 6 // Full house
	} else if isFlush {
		return 5 // Flush
	} else if isStraight {
		return 4 // Straight
	} else if g.hasOfAKind(values, 3) {
		return 3 // Three of a kind
	} else if g.countPairs(values) == 2 {
		return 2 // Two pair
	} else if g.hasOfAKind(values, 2) {
		return 1 // One pair
	}

	return 0 // High card
}

// hasOfAKind checks if hand has n cards of the same value
func (g *CardGame) hasOfAKind(values map[int]int, n int) bool {
	for _, count := range values {
		if count == n {
			return true
		}
	}
	return false
}

// countPairs counts the number of pairs in hand
func (g *CardGame) countPairs(values map[int]int) int {
	pairs := 0
	for _, count := range values {
		if count == 2 {
			pairs++
		}
	}
	return pairs
}

// determinePokerWinner determines the winner of Poker round
func (g *CardGame) determinePokerWinner() {
	bestRank := -1
	var winners []int

	for i, player := range g.Players {
		if player.Score > bestRank {
			bestRank = player.Score
			winners = []int{i}
		} else if player.Score == bestRank {
			winners = append(winners, i)
		}
	}

	handNames := []string{"High Card", "One Pair", "Two Pair", "Three of a Kind",
		"Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"}

	if len(winners) == 1 {
		winner := &g.Players[winners[0]]
		winner.Wins++
		handName := "High Card"
		if bestRank < len(handNames) {
			handName = handNames[bestRank]
		}
		fmt.Printf("🏆 %s wins with %s!\n", winner.Name, handName)
	} else {
		fmt.Printf("🤝 Tie between %d players!\n", len(winners))
	}
}

// playHighCardRound plays a High Card round
func (g *CardGame) playHighCardRound() {
	fmt.Println("🎯 High Card Round!")

	for i := range g.Players {
		player := &g.Players[i]
		if len(player.Hand) > 0 {
			card := player.Hand[0]
			fmt.Printf("%s drew: %s (Value: %d)\n", player.Name, card, card.Value)
			player.Score = card.Value
		}
	}

	g.determineHighCardWinner()
}

// determineHighCardWinner determines the winner of High Card round
func (g *CardGame) determineHighCardWinner() {
	bestValue := 0
	var winners []int

	for i, player := range g.Players {
		if player.Score > bestValue {
			bestValue = player.Score
			winners = []int{i}
		} else if player.Score == bestValue {
			winners = append(winners, i)
		}
	}

	if len(winners) == 1 {
		winner := &g.Players[winners[0]]
		winner.Wins++
		fmt.Printf("🏆 %s wins with %d!\n", winner.Name, bestValue)
	} else {
		fmt.Printf("🤝 Tie between %d players with %d!\n", len(winners), bestValue)
	}

	// Reset hands for next round
	for i := range g.Players {
		g.Players[i].Hand = make([]Card, 0)
		g.Players[i].IsActive = true
	}
}

// printHand prints a player's hand
func (g *CardGame) printHand(hand []Card) {
	fmt.Print("Hand: [")
	for i, card := range hand {
		if i > 0 {
			fmt.Print(", ")
		}
		fmt.Print(card)
	}
	fmt.Println("]")
}

// PrintGameState displays current game state
func (g *CardGame) PrintGameState() {
	fmt.Println("\n📊 Current Game State:")
	fmt.Println("=" + string(make([]rune, 60, 60)) + "=")
	fmt.Printf("Game Type: %s | Round: %d | Cards in Deck: %d\n",
		g.GameType, g.Round, len(g.Deck.Cards))

	for _, player := range g.Players {
		status := "Active"
		if !player.IsActive {
			status = "Inactive"
		}
		fmt.Printf("Player: %-10s | Score: %-4d | Wins: %-2d | Status: %s | Cards: %d\n",
			player.Name, player.Score, player.Wins, status, len(player.Hand))
	}
	fmt.Println()
}

// GetWinner returns the player with the most wins
func (g *CardGame) GetWinner() *CardPlayer {
	if len(g.Players) == 0 {
		return nil
	}

	winner := &g.Players[0]
	for i := range g.Players {
		if g.Players[i].Wins > winner.Wins {
			winner = &g.Players[i]
		}
	}
	return winner
}

// EndGame ends the card game and declares winner
func (g *CardGame) EndGame() {
	g.GameActive = false
	winner := g.GetWinner()

	fmt.Println("\n🏁 Game Over!")
	fmt.Println("=" + string(make([]rune, 50, 50)) + "=")

	if winner != nil {
		fmt.Printf("🥇 Overall Winner: %s with %d wins!\n", winner.Name, winner.Wins)
	}

	fmt.Println("\nFinal Standings:")
	// Sort players by wins
	players := make([]CardPlayer, len(g.Players))
	copy(players, g.Players)

	sort.Slice(players, func(i, j int) bool {
		return players[i].Wins > players[j].Wins
	})

	for i, player := range players {
		fmt.Printf("%d. %s - %d wins (Score: %d)\n",
			i+1, player.Name, player.Wins, player.Score)
	}
}

// RunCardGameSimulation runs a complete card game simulation
func RunCardGameSimulation() {
	rand.Seed(time.Now().UnixNano())

	fmt.Println("🃏 Welcome to the Discord Bot Card Game Simulation!")
	fmt.Println("=" + string(make([]rune, 55, 55)) + "=")

	// Create different types of card games
	gameTypes := []string{"HighCard", "BlackJack", "Poker"}
	selectedGame := gameTypes[rand.Intn(len(gameTypes))]

	// Create new card game
	game := NewCardGame(selectedGame)

	// Add players
	playerNames := []string{"Alice", "Bob", "Charlie", "Diana"}
	for _, name := range playerNames {
		game.AddPlayer(name)
	}

	// Start the game
	game.StartGame()

	// Play multiple rounds
	maxRounds := 5
	if selectedGame == "Poker" {
		maxRounds = 3 // Fewer rounds for poker due to complexity
	}

	for round := 1; round <= maxRounds; round++ {
		game.PlayRound()
		game.PrintGameState()

		// Add some delay for readability
		time.Sleep(1 * time.Second)

		// Reshuffle deck if running low on cards
		if len(game.Deck.Cards) < 10 {
			fmt.Println("🔄 Reshuffling deck...")
			game.Deck = NewStandardDeck()
			game.Deck.Shuffle()
		}
	}

	// End the game
	game.EndGame()
}

func main() {
	RunCardGameSimulation()
}