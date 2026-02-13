import {
    Table,
    TableHeader,
    TableColumn,
    TableBody,
    TableRow,
    TableCell,
    Tooltip,
    Pagination,
} from "@heroui/react";
import { useState, useEffect, useCallback, useMemo } from "react";
import type { Candidate } from "../types/candidate";
import CandidateService from "../services/CandidateService";
import { EyeIcon, DeleteIcon, EditIcon } from "../assets/icons";
import { Link } from "react-router-dom";

const columns = [
    { name: "NAME", uid: "name" },
    { name: "EMAIL", uid: "email" },
    { name: "PHONE", uid: "phone" },
    { name: "LOCATION", uid: "location" },
    { name: "ROLE", uid: "role" },
    { name: "EXPERIENCE", uid: "experience" },
    { name: "ACTIONS", uid: "actions" },
];

interface TableCandidatesProps {
    searchTerm: string;
}

export const TableCandidates = ({ searchTerm }: TableCandidatesProps) => {
    const [candidates, setCandidates] = useState<Candidate[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const rowsPerPage = 6;

    const filteredCandidates = useMemo(() => {
        if (!searchTerm.trim()) {
            return candidates;
        }

        const lowerSearch = searchTerm.toLowerCase();
        return candidates.filter((candidate) => {
            return (
                candidate.name?.toLowerCase().includes(lowerSearch) ||
                candidate.email?.toLowerCase().includes(lowerSearch) ||
                candidate.phone?.toLowerCase().includes(lowerSearch) ||
                candidate.location?.toLowerCase().includes(lowerSearch) ||
                candidate.role?.toLowerCase().includes(lowerSearch) ||
                candidate.experience?.toLowerCase().includes(lowerSearch)
            );
        });
    }, [candidates, searchTerm]);

    const pages = Math.ceil(filteredCandidates.length / rowsPerPage);

    const items = useMemo(() => {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        return filteredCandidates.slice(start, end);
    }, [page, filteredCandidates]);

    useEffect(() => {
        setPage(1);
    }, [searchTerm]);

    useEffect(() => {
        const fetchCandidates = async () => {
            setLoading(true);
            try {
                const data = await CandidateService.listCandidates();
                setCandidates(data);
            } catch (err) {
                setError("No se pudieron cargar los candidatos. Intenta más tarde.");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchCandidates();
    }, []);

    const handleDelete = async (id: string) => {
        if (!window.confirm("¿Estás seguro de eliminar este candidato?")) return;

        try {
            await CandidateService.deleteCandidate(id);
            setCandidates((prev) => prev.filter((c) => c.id !== id));
            alert("Candidato eliminado con éxito");
        } catch (err) {
            alert("Error al eliminar el candidato");
            console.error(err);
        }
    };

    const renderCell = useCallback((candidate: Candidate, columnKey: React.Key) => {
        const cellValue = candidate[columnKey as keyof Candidate];

        switch (columnKey) {
            case "name":
                return (
                    <div className="flex flex-col">
                        <p className="text-bold text-sm capitalize">{cellValue}</p>
                    </div>
                );
            case "email":
                return (
                    <div className="flex flex-col">
                        <p className="text-bold text-sm capitalize">{cellValue}</p>
                    </div>
                );
            case "phone":
                return (
                    <div className="flex flex-col">
                        <p className="text-bold text-sm capitalize">{cellValue}</p>
                    </div>
                );
            case "location":
                return (
                    <div className="flex flex-col">
                        <p className="text-bold text-sm capitalize">{cellValue}</p>
                    </div>
                );
            case "role":
                return (
                    <div className="flex flex-col">
                        <p className="text-bold text-sm capitalize">{cellValue}</p>
                        <p className="text-bold text-sm capitalize text-default-400">{candidate.headline}</p>
                    </div>
                );
            case "experience":
                return (
                    <div className="flex flex-col">
                        <p className="text-bold text-sm capitalize">{cellValue}</p>
                    </div>
                );
            case "actions":
                return (
                    <div className="relative flex items-center gap-2">
                        <Tooltip content="Details">
                            <Link to={`/${candidate.id}/insight`}>
                                <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
                                    <EyeIcon />
                                </span>
                            </Link>
                        </Tooltip>
                        <Tooltip content="Edit user">
                            <Link to={`/edit/${candidate.id}`}>
                                <span className="text-lg text-default-400 cursor-pointer active:opacity-50">
                                    <EditIcon />
                                </span>
                            </Link>
                        </Tooltip>
                        <Tooltip color="danger" content="Delete user">
                            <button onClick={() => handleDelete(candidate.id)}>
                                <span className="text-lg text-danger cursor-pointer active:opacity-50">
                                    <DeleteIcon />
                                </span>
                            </button>
                        </Tooltip>
                    </div>
                );
            default:
                return cellValue;
        }
    }, []);

    return (
        <Table
            isStriped
            aria-label="Table of candidates with pagination"
            bottomContent={
                <div className="flex w-full justify-center">
                    <Pagination
                        isCompact
                        showControls
                        showShadow
                        color="secondary"
                        page={page}
                        total={pages}
                        onChange={(page) => setPage(page)}
                    />
                </div>
            }
            classNames={{
                wrapper: "min-h-[222px]",
            }}

        >
            <TableHeader columns={columns}>
                {(columns) => (
                    <TableColumn key={columns.uid} align={columns.uid === "actions" ? "center" : "start"}>
                        {columns.name}
                    </TableColumn>
                )}
            </TableHeader>
            <TableBody
                items={items}
                emptyContent={"No rows to display."}
            >
                {!loading && !error ? (item) => (
                    <TableRow key={item.id}>
                        {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
                    </TableRow>
                ) : (
                    <>{[]}</>
                )}
            </TableBody>
        </Table>
    )
}
