import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
    Button,
    Tooltip,
    Divider,
    ScrollShadow,
    Avatar,
    cn,
} from "@heroui/react";
import { HomeIcon, UsersIcon, LogoutIcon } from "../../assets/icons";

interface AppSidebarProps {
    className?: string;
}

const menuItems = [
    { key: "dashboard", label: "Dashboard", icon: HomeIcon, path: "/" },
    { key: "create-candidate", label: "Crear Candidato", icon: UsersIcon, path: "/create" },
];

const MenuIcon = ({ className }: { className?: string }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
    </svg>
);

const ChevronLeftIcon = ({ className }: { className?: string }) => (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
    </svg>
);

export const AppSidebar = ({ className }: AppSidebarProps) => {
    const location = useLocation();
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [isMobileOpen, setIsMobileOpen] = useState(false);

    const isActive = (path: string) =>
        location.pathname === path ||
        (path === "/" && location.pathname === "");

    const handleNavigation = () => {
        setIsMobileOpen(false);
    };

    const SidebarContent = ({ isMobile = false }: { isMobile?: boolean }) => {
        const collapsed = !isMobile && isCollapsed;

        return (
            <div className="flex h-full flex-col">
                <div className={cn(
                    "flex items-center gap-3 px-4 py-5 transition-all duration-300",
                    collapsed && "justify-center px-2"
                )}>
                    <Avatar
                        src=""
                        size={collapsed ? "sm" : "md"}
                        color="primary"
                        isBordered
                        className="shrink-0"
                    />
                    {!collapsed && (
                        <div className="overflow-hidden">
                            <p className="font-semibold text-sm truncate">wTreData SAS</p>
                            <p className="text-tiny text-default-500 truncate">Admin Panel</p>
                        </div>
                    )}
                </div>

                <Divider />

                {!isMobile && (
                    <div className="px-2 py-2">
                        <Button
                            isIconOnly={collapsed}
                            size="sm"
                            variant="light"
                            onPress={() => setIsCollapsed(!isCollapsed)}
                            className="w-full"
                        >
                            {collapsed ? (
                                <MenuIcon className="h-5 w-5" />
                            ) : (
                                <>
                                    <ChevronLeftIcon className="h-5 w-5" />
                                    <span className="ml-2">Colapsar</span>
                                </>
                            )}
                        </Button>
                    </div>
                )}

                <Divider />

                <div className="flex-1 py-4">
                    <nav className="flex flex-col gap-4 items-center w-full">
                        {menuItems.map((item) => {
                            const Icon = item.icon;
                            const active = isActive(item.path);

                            const navButton = (
                                <Link
                                    to={item.path}
                                    onClick={handleNavigation}
                                    className={cn(
                                        "flex items-center gap-2 w-full rounded-lg p-2",
                                        active && "bg-primary/10 text-primary font-semibold",
                                        collapsed && "justify-center"
                                    )}
                                    color={active ? "primary" : "default"}
                                >
                                    {!collapsed && <Icon className="h-5 w-5" />}
                                    {collapsed ? (
                                        <Icon className="h-5 w-5" />
                                    ) : (
                                        item.label
                                    )}
                                </Link>
                            );

                            if (collapsed) {
                                return (
                                    <Tooltip
                                        key={item.key}
                                        content={item.label}
                                        placement="right"
                                    >
                                        {navButton}
                                    </Tooltip>
                                );
                            }

                            return <div key={item.key}>{navButton}</div>;
                        })}
                    </nav>
                </div>

                <div className="p-3 mt-auto">
                    <Tooltip
                        content={collapsed ? "Cerrar Sesión" : ""}
                        placement="right"
                        isDisabled={!collapsed}
                    >
                        <Button
                            variant="light"
                            color="danger"
                            fullWidth
                            isIconOnly={collapsed}
                            startContent={!collapsed && <LogoutIcon className="h-5 w-5" />}
                        >
                            {collapsed ? (
                                <LogoutIcon className="h-5 w-5" />
                            ) : (
                                "Cerrar Sesión"
                            )}
                        </Button>
                    </Tooltip>
                </div>
            </div>
        );
    };

    return (
        <>
            <button
                onClick={() => setIsMobileOpen(true)}
                className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-content1 border border-divider shadow-md"
                aria-label="Abrir menú"
            >
                <MenuIcon className="h-6 w-6" />
            </button>

            {isMobileOpen && (
                <div
                    className="lg:hidden fixed inset-0 bg-black/50 z-40 transition-opacity"
                    onClick={() => setIsMobileOpen(false)}
                />
            )}

            <aside
                className={cn(
                    "lg:hidden fixed inset-y-0 left-0 z-50 w-64 bg-content1 border-r border-divider transform transition-transform duration-300 ease-in-out",
                    isMobileOpen ? "translate-x-0" : "-translate-x-full"
                )}
            >
                <SidebarContent isMobile />
            </aside>

            <aside
                className={cn(
                    "hidden lg:block h-screen shrink-0 border-r border-divider bg-content1 sticky top-0 transition-all duration-300",
                    isCollapsed ? "w-16" : "w-64",
                    className
                )}
            >
                <SidebarContent />
            </aside>
        </>
    );
};