import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import '../App.css'

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

  if (!product) {
    return (
      <div className="page">
        <div className="loading-text">Loading...</div>
      </div>
    )
  }

  const listingsWithUnit = product.listings.filter((l) => l.price_per_unit != null)
  const best = listingsWithUnit.length > 0
    ? listingsWithUnit.reduce((a, b) => (a.price_per_unit < b.price_per_unit ? a : b))
    : product.listings.reduce(
        (a, b) => (a?.raw_price != null && (b.raw_price == null || a.raw_price < b.raw_price) ? a : b),
        null
      )

  return (
    <div className="page">
      <Link to="/" className="back-link">Back to search</Link>

      <div className="product-header">
        <h1>{product.brand} - {product.product_name}</h1>
        <div className="product-meta">
          {product.quantity_value && product.quantity_unit
            ? `${product.quantity_value} ${product.quantity_unit}`
            : 'Size not recorded for this product'}
          {product.shade_or_color ? ` - ${product.shade_or_color}` : ''}
        </div>
      </div>

      <div className="section-label">
        {product.listings.length} listing{product.listings.length !== 1 ? 's' : ''}
      </div>

      {product.listings.length === 0 && (
        <div className="empty-state">No listings recorded for this product yet.</div>
      )}

      {product.listings.map(function (listing) {
        const isBest = best && listing.id === best.id
        const rowClass = isBest ? "listing-row best-deal" : "listing-row"

        return (
          <div key={listing.id} className={rowClass}>
            <div>
              <div className="listing-retailer">{listing.retailer_name}</div>
              <div className="listing-seller">{listing.seller_name}</div>
            </div>

            <div className="listing-prices">
              <div className="listing-price">
                {listing.raw_price != null ? "Rs " + listing.raw_price : "Price unavailable"}
              </div>
              {listing.price_per_unit != null && (
                <div className="listing-price-per-unit">
                  {"Rs " + listing.price_per_unit + " / " + product.quantity_unit}
                </div>
              )}
            </div>

            <a href={listing.product_url} target="_blank" rel="noreferrer" className="listing-link">View listing</a>
          </div>
        )
      })}
    </div>
  )
}

export default Compare