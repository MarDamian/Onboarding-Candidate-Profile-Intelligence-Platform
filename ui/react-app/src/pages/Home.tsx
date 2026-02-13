import { TableCandidates } from "../components/TableCandidates"

interface HomePageProps {
  searchTerm: string;
}

export const HomePage = ({ searchTerm }: HomePageProps) => {
  return (
    <TableCandidates searchTerm={searchTerm} />
  )
}
