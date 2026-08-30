import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'

const API_BASE = 'http://localhost:8000'

function Compare() {
  const { id } = useParams()
  const [product, setProduct] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/products/${id}`)
      .then((res) => res.json())
      .then((data) => setProduct(data))
      .catch((err) => console.error('Failed to load product:', err))
  }, [id])

  if (!product) return <p style={{ padding: 40 }}>Loading...</p>

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <Link to="/">&larr; Back to search</Link>
      <h1>{product.brand} — {product.product_name}</h1>
      <p style={{ color: '#666' }}>
        {product.quantity_value} {product.quantity_unit}
        {product.shade_or_color ? ` · ${product.shade_or_color}` : ''}
      </p>

      <h3>Compare listings</h3>
      {product.listings.length === 0 && <p>No matched listings yet.</p>}

      {product.listings.map((listing) => (
        <div
          key={listing.id}
          style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, marginBottom: 12 }}
        >
          <strong>{listing.retailer_name}</strong>
          <div>Price: ₹{listing.raw_price}</div>
          {listing.price_per_unit && (
            <div style={{ color: '#2a7a2a', fontWeight: 600 }}>
              ₹{listing.price_per_unit} / {product.quantity_unit}
            </div>
          )}
          <div style={{ fontSize: 13, color: '#999' }}>Seller: {listing.seller_name}</div>
          <a href={listing.product_url} target="_blank" rel="noreferrer">
            View on {listing.retailer_name}
          </a>
        </div>
      ))}
    </div>
  )
}

export default Compare