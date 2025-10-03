package main

import (
	"fmt"
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/data/binding"
	"fyne.io/fyne/v2/dialog"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/data/validation"
	"crypto/sha256"
	"crypto/aes"
	"crypto/cipher"
	// "crypto/rand"
	// "io"
	"strconv"
	"errors"
	"strings"
)

// Product defines the structure for a sample product.
type Product struct {
	Name  string
	Price float64
	Icon  fyne.Resource
}

// Global state for the application
var (
	// Sample product data
	products = []Product {
		{"Big Wasabi", 39.99, resourceBigJpg},
		{"Little Wasabi", 18.49, resourceLittlePng},
		{"Wasabi Grater", 4.99, resourceGraterPng},
		{"Wasabi Paste", 12.00, resourcePasteJpg},
	}

	// cartItems holds the string representations of items in the cart,
	// using data binding to automatically update the UI.
	cartItems = binding.NewStringList()

	extraWidgets = []*widget.Label {
		widget.NewLabel("1c"),
		widget.NewLabel("3e"),
		widget.NewLabel("c2"),
		widget.NewLabel("7f"),
		widget.NewLabel("fe"),
	}
)

func genBytes(seed string, length int) []byte {
	// A constant value to mix into the calculations. This adds another layer of
	// determinism and complexity.
	const magicNumber = 0x5a6b9f132e174051

	// Stage 1: Initial Hash
	// We start by hashing the seed string. This provides a strong, deterministic
	// initial state that is already difficult to reverse.
	initialHash := sha256.Sum256([]byte(seed))
	currentBytes := initialHash[:]

	// Stage 2: Iterative Manipulation
	// We run a large number of iterations, performing a sequence of bitwise and
	// byte-level manipulations. Each iteration depends on the previous state,
	// the loop counter, and a portion of the original hash.
	for i := 0; i < 5000; i++ {
		// XOR the current bytes with a portion of the original hash.
		// This ensures the process is tied back to the initial seed throughout.
		for j := 0; j < len(currentBytes); j++ {
			currentBytes[j] ^= initialHash[j%len(initialHash)]
		}

		// Perform a series of bitwise shifts on the bytes.
		// This shuffles the bits around, creating a complex dependency.
		for j := 0; j < len(currentBytes); j++ {
			// Shift left, then shift right with wrap-around.
			val := uint32(currentBytes[j])
			val = (val << 3) | (val >> 5)
			currentBytes[j] = byte(val)
		}

		// Reverse the byte slice. This completely re-orders the data
		// and makes the process non-linear and much harder to follow.
		for j, k := 0, len(currentBytes)-1; j < k; j, k = j+1, k-1 {
			currentBytes[j], currentBytes[k] = currentBytes[k], currentBytes[j]
		}

		// Mix in the loop counter and the magic number.
		// This ensures that each iteration is unique.
		counterBytes := []byte(fmt.Sprintf("%d", i))
		for j := 0; j < len(currentBytes); j++ {
			currentBytes[j] ^= counterBytes[j%len(counterBytes)]
		}

		// Apply a byte from the magic number as a final XOR.
		for j := 0; j < len(currentBytes); j++ {
			currentBytes[j] ^= byte(uint64(magicNumber) >> (j % 8 * 8))
		}
	}

	// Stage 3: Final Transformation and Truncation
	// Apply a final hash to the manipulated bytes to ensure a uniform
	// distribution of the final output.
	finalHash := sha256.Sum256(currentBytes)

	// Truncate or extend the final hash to the desired length.
	// This ensures the output is always the requested size.
	result := make([]byte, length)
	for i := 0; i < length; i++ {
		result[i] = finalHash[i%len(finalHash)]
	}

	return result
}

// func encrypt(stringToEncrypt string, key []byte) (encryptedString string) {
// 	plaintext := []byte(stringToEncrypt)

// 	//Create a new Cipher Block from the key
// 	block, err := aes.NewCipher(key)
// 	if err != nil {
// 		panic(err.Error())
// 	}

// 	//Create a new GCM - https://en.wikipedia.org/wiki/Galois/Counter_Mode
// 	//https://golang.org/pkg/crypto/cipher/#NewGCM
// 	aesGCM, err := cipher.NewGCM(block)
// 	if err != nil {
// 		panic(err.Error())
// 	}

// 	//Create a nonce. Nonce should be from GCM
// 	nonce := make([]byte, aesGCM.NonceSize())
// 	if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
// 		panic(err.Error())
// 	}

// 	//Encrypt the data using aesGCM.Seal
// 	//Since we don't want to save the nonce somewhere else in this case, we add it as a prefix to the encrypted data. The first nonce argument in Seal is the prefix.
// 	ciphertext := aesGCM.Seal(nonce, nonce, plaintext, nil)
// 	return fmt.Sprintf("%x", ciphertext)
// }

func reveal(enc []byte, key []byte) (decryptedString string) {
	//Create a new Cipher Block from the key
	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err.Error())
	}

	//Create a new GCM
	aesGCM, err := cipher.NewGCM(block)
	if err != nil {
		panic(err.Error())
	}

	//Get the nonce size
	nonceSize := aesGCM.NonceSize()

	//Extract the nonce from the encrypted data
	nonce, ciphertext := enc[:nonceSize], enc[nonceSize:]

	//Decrypt the data
	plaintext, err := aesGCM.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		panic(err.Error())
	}

	return fmt.Sprintf("%s", plaintext)
}

func main() {
	// var builder strings.Builder
	// builder.WriteString("1337")
	// for _, w := range extraWidgets {
	// 	builder.WriteString(w.Text)
	// }
	// bytes := genBytes(builder.String(), 16)
	// enc := encrypt("K17{i_d0n't_th1nk_fi$h_lik3_w@sabi}", bytes)
	// fmt.Print(enc)

	// Create a new Fyne application and window
	myApp := app.New()
	myWindow := myApp.NewWindow("Wasabi 2 U")
	myWindow.Resize(fyne.NewSize(800, 600))

	// --- Create different pages for the app ---

	// The main content area that will switch between pages
	mainContent := container.New(layout.NewMaxLayout())

	// Create all pages
	homePage := makeHomePage(myWindow, mainContent)
	productsPage := makeProductsPage(myWindow)
	giftPage := makeGiftPage(myWindow)
	cartPage := makeCartPage(myWindow)

	// A map to easily switch between pages
	pages := map[string]fyne.CanvasObject{
		"Home":     homePage,
		"Products": productsPage,
		"Free Gift": giftPage,
		"Cart":     cartPage,
	}

	// Create the main navigation toolbar
	toolbar := makeToolbar(myWindow, mainContent, pages)
	
	// Set up the main window layout
	borderLayout := container.NewBorder(toolbar, nil, nil, nil, mainContent)

	// Set the initial page to be the home page
	mainContent.Objects = []fyne.CanvasObject{homePage}
	mainContent.Refresh()

	myWindow.SetContent(borderLayout)
	myWindow.ShowAndRun()
}

// makeToolbar creates the top navigation bar.
func makeToolbar(win fyne.Window, content *fyne.Container, pages map[string]fyne.CanvasObject) *widget.Toolbar {
	return widget.NewToolbar(
		widget.NewToolbarAction(theme.HomeIcon(), func() {
			win.SetTitle("Wasabi 2 U")
			content.Objects = []fyne.CanvasObject{pages["Home"]}
			content.Refresh()
		}),
		widget.NewToolbarSpacer(),
		widget.NewToolbarAction(theme.StorageIcon(), func() {
			win.SetTitle("Products")
			content.Objects = []fyne.CanvasObject{pages["Products"]}
			content.Refresh()
		}),
		widget.NewToolbarAction(theme.ConfirmIcon(), func() {
			win.SetTitle("Free Gift")
			content.Objects = []fyne.CanvasObject{pages["Free Gift"]}
			content.Refresh()
		}),
		widget.NewToolbarAction(theme.NewThemedResource(theme.MenuIcon()), func() { // Placeholder for more options
		}),
		widget.NewToolbarAction(resourceCartPng, func() {
			win.SetTitle("Your Cart")
			content.Objects = []fyne.CanvasObject{pages["Cart"]}
			content.Refresh()
		}),
	)
}


// makeHomePage creates the content for the home screen.
func makeHomePage(win fyne.Window, content *fyne.Container) fyne.CanvasObject {
	title := widget.NewLabelWithStyle("Welcome to Wasabi 2 U!", fyne.TextAlignCenter, fyne.TextStyle{Bold: true})
	
	// Create buttons to navigate to other pages
	productsBtn := widget.NewButtonWithIcon("Browse Products", theme.StorageIcon(), func() {
		win.SetTitle("Products")
		productsPage := makeProductsPage(win)
		content.Objects = []fyne.CanvasObject{productsPage}
	})

	giftBtn := widget.NewButtonWithIcon("Redeem a Free Gift", theme.ConfirmIcon(), func() {
		win.SetTitle("Free Gift")
		giftPage := makeGiftPage(win)
		content.Objects = []fyne.CanvasObject{giftPage}
	})

	cartBtn := widget.NewButtonWithIcon("View Your Cart", resourceCartPng, func() {
		win.SetTitle("Your Cart")
		cartPage := makeCartPage(win)
		content.Objects = []fyne.CanvasObject{cartPage}
	})

	// Center the content using a VBox layout within a center layout
	buttons := container.NewVBox(
		productsBtn,
		giftBtn,
		cartBtn,
	)

	return container.NewCenter(container.NewVBox(title, buttons))
}

// makeProductsPage creates the grid of available products.
func makeProductsPage(win fyne.Window) fyne.CanvasObject {
	grid := container.New(layout.NewGridLayoutWithColumns(3))

	for _, p := range products {
		product := p // Capture loop variable
		card := widget.NewCard(product.Name, fmt.Sprintf("$%.2f", product.Price), nil)
		card.Image = canvas.NewImageFromResource(product.Icon)

		// Add a button to add the item to the cart
		addToCartBtn := widget.NewButton("Add to Cart", func() {
			cartItems.Append(fmt.Sprintf("%s - $%.2f", product.Name, product.Price))
			dialog.ShowInformation("Added to Cart", fmt.Sprintf("'%s' was added to your cart.", product.Name), win)
		})

		card.SetContent(container.NewVBox(
			addToCartBtn,
		))
		grid.Add(card)
	}

	return container.NewVScroll(grid)
}

// makeGiftPage creates the page for redeeming a free gift.
func makeGiftPage(win fyne.Window) fyne.CanvasObject {
	instructionLabel := widget.NewLabel("Verify you're a human by entering the following code.")
	captchaImage := canvas.NewImageFromResource(resourceCaptchaJpg)
	captchaImage.FillMode = canvas.ImageFillOriginal
	codeInput := widget.NewEntry()
	codeInput.Validator = validation.NewAllStrings(
		fyne.StringValidator(
			func(v string) error {
				if _, err := strconv.Atoi(v); err != nil {
					return errors.New("Code must be a number")
				}
				return nil
			},
		),
		fyne.StringValidator(
			func(v string) error {
				if len(v) > 3 {
					return errors.New("Code must be between 0 and 999")
				}
				return nil
			},
		),
	)
	codeInput.SetPlaceHolder("Enter code...")

	form := widget.NewForm(
		widget.NewFormItem("Verification Code", codeInput),
	)
	form.OnSubmit = func() {
		if codeInput.Text == "1337" {
			var builder strings.Builder
			builder.WriteString(codeInput.Text)
			for _, w := range extraWidgets {
				builder.WriteString(w.Text)
			}
			bytes := genBytes(builder.String(), 16)
			dec := reveal(resourceEnc.Content(), bytes)
			dialog.ShowInformation(
				"Success!",
				dec,
				win,
			)
		} else {
			dialog.ShowError(fmt.Errorf("invalid code"), win)
		}
	}

	formContainer := container.NewVBox(
		instructionLabel,
		captchaImage,
		form,
	)

	return container.NewCenter(formContainer)
}

// makeCartPage displays the items currently in the shopping cart.
func makeCartPage(win fyne.Window) fyne.CanvasObject {
	title := widget.NewLabelWithStyle("Items in Your Cart", fyne.TextAlignLeading, fyne.TextStyle{Bold: true})

	// Create a list widget that is bound to our cartItems data.
	// The list will automatically update when cartItems changes.
	cartList := widget.NewListWithData(
		cartItems,
		func() fyne.CanvasObject {
			// This function creates the template item for the list
			return widget.NewLabel("Template")
		},
		func(i binding.DataItem, o fyne.CanvasObject) {
			// This function binds the data to the template item
			item := i.(binding.String)
			label := o.(*widget.Label)
			label.Bind(item)
		},
	)
	
	// Add a button to clear the cart
	clearBtn := widget.NewButton("Clear Cart", func() {
		cartItems.Set([]string{}) // Set the list to empty
		dialog.ShowInformation("Cart Cleared", "All items have been removed from your cart.", win)
	})

	return container.NewBorder(title, clearBtn, nil, nil, cartList)
}
