
<style>
.arrow-float {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2.5rem;
  color: white;
  background-color: #2c3e50;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  z-index: 999;
  transition: background 0.2s ease;
}

.arrow-float:hover {
  background-color: #34495e;
}

.arrow-float.left {
  left: 20px;
}

.arrow-float.right {
  right: 20px;
}

</style>

<a href="/next" class="arrow-float left" aria-label="Previous page">←</a>
<a href="/" class="arrow-float right" aria-label="Next page">→</a>