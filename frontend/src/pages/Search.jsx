import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE = 'http://localhost:8000'

function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  // Calls our FastAPI backend's /products/search endpoint.
  // This searches OUR catalog (matched_product table) --
  // not live retailer sites -- exactly as we discussed.
  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/products/search?q=${encodeURIComponent(query)}`)
      const data = await res.json()
      setResults(data)
    } catch (err) {
      console.error('Search failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: '60px auto', fontFamily: 'sans-serif' }}>
      <h1>Shopping Comparison</h1>
      <form onSubmit={handleSearch} style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search e.g. Huda Beauty mascara"
          style={{ flex: 1, padding: 10, fontSize: 16 }}
        />
        <button type="submit" style={{ padding: '10px 20px' }}>Search</button>
      </form>

      {loading && <p>Searching...</p>}

      <div style={{ marginTop: 20 }}>
        {results.map((product) => (
          <div
            key={product.id}
            onClick={() => navigate(`/product/${product.id}`)}
            style={{
              border: '1px solid #ddd',
              borderRadius: 8,
              padding: 16,
              marginBottom: 12,
              cursor: 'pointer',
            }}
          >
            <strong>{product.brand}</strong> — {product.product_name}
            <div style={{ color: '#666', fontSize: 14 }}>
              {product.quantity_value} {product.quantity_unit}
              {product.shade_or_color ? ` · ${product.shade_or_color}` : ''}
            </div>
            <div style={{ fontSize: 13, color: '#999' }}>
              {product.listings.length} listing(s) found
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Search
