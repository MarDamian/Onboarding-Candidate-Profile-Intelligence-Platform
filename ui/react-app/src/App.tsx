import { Routes, Route } from 'react-router-dom'
import './App.css'
import { CreatePage } from './pages/Create'
import { EditPage } from './pages/Edit'
import { ShowPage } from './pages/Show'
import { ListPage } from './pages/List'

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<ListPage />} />
        <Route path="/create" element={<CreatePage />} />
        <Route path="/edit/:id" element={<EditPage />} />
        <Route path="/show/:id" element={<ShowPage />} />
      </Routes>
    </>
  )
}

export default App
