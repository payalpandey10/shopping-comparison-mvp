import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../App.css'

const API_BASE = 'http://localhost:8000'

function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)
  const navigate = useNavigate()

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setSearched(true)
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
    <div className="page">
      <div className="masthead">
        <h1>Price Ledger</h1>
        <span className="tagline">compare the real price, not just the listed one</span>
      </div>

      <form className="search-form" onSubmit={handleSearch}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search a product — e.g. Maybelline mascara"
        />
        <button type="submit">Search</button>
      </form>

      {loading && <div className="status-line">Searching…</div>}

      {!loading && searched && (
        <div className="status-line">
          {results.length} result{results.length !== 1 ? 's' : ''} for "{query}"
        </div>
      )}

      <div className="result-list">
        {results.map((product) => (
          <div
            key={product.id}
            className="result-row"
            onClick={() => navigate(`/product/${product.id}`)}
          >
            <div className="result-main">
              <span className="brand">{product.brand}</span>
              {' — '}
              <span className="product">{product.product_name}</span>
              <div className="result-meta">
                {product.quantity_value && product.quantity_unit
                  ? `${product.quantity_value} ${product.quantity_unit}`
                  : 'Size not recorded'}
                {product.shade_or_color ? ` · ${product.shade_or_color}` : ''}
              </div>
            </div>
            <div className="result-count">
              {product.listings.length} listing{product.listings.length !== 1 ? 's' : ''}
            </div>
          </div>
        ))}

        {!loading && searched && results.length === 0 && (
          <div className="empty-state">
            Nothing in the catalog matches "{query}" yet. Try a different brand or product name.
          </div>
        )}
      </div>
    </div>
  )
}

export default Search