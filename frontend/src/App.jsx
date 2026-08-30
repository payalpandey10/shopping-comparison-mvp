import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Search from './pages/Search.jsx'
import Compare from './pages/Compare.jsx'

// This is where our two main screens (from Stage 1's plan) live:
// Search -> user types a product, sees matched_product results
// Compare -> user picks one, sees all raw_listings side by side
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Search />} />
        <Route path="/product/:id" element={<Compare />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
