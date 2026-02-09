import {
    Navbar as HeroUINavbar,
    NavbarBrand,
    NavbarContent,
    NavbarItem,
    Input,
    cn,
} from "@heroui/react";
import { SearchIcon } from "../../assets/icons";

interface AppNavbarProps {
    projectName?: string;
    className?: string;
    searchTerm: string;
    onSearchChange: (value: string) => void;
}

export default function AppNavbar({
    projectName = "Onboarding Intelligence",
    className,
    searchTerm,
    onSearchChange,
}: AppNavbarProps) {
    return (
        <HeroUINavbar
            isBordered
            className={cn(
                "border-b border-divider bg-content1/70 backdrop-blur-lg",
                className
            )}
            position="sticky"
            height="4rem"
        >
            <NavbarContent justify="start">
                <NavbarItem>
                    <NavbarBrand>
                        <p className="font-bold text-xl text-foreground">
                            {projectName}
                        </p>
                    </NavbarBrand>
                </NavbarItem>
            </NavbarContent>

            <NavbarContent justify="end" className="gap-4 sm:gap-6">
                <NavbarItem className="flex-1">
                    <Input
                        aria-label="Buscar"
                        placeholder="Buscar candidatos, reportes..."
                        size="sm"
                        startContent={
                            <SearchIcon className="text-default-400 pointer-events-none shrink-0 text-base" />
                        }
                        classNames={{
                            inputWrapper: "bg-default-100/70 dark:bg-default-50/70 border-default-200",
                            input: "text-foreground placeholder:text-default-400",
                        }}
                        value={searchTerm}
                        onValueChange={onSearchChange}
                    />
                </NavbarItem>
            </NavbarContent>
        </HeroUINavbar>
    );
}