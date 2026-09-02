"use client"

import * as React from "react"
import { useTheme } from "next-themes"
import { Moon, Sun, Monitor, LogOut, User } from "lucide-react"
import { useAuth } from "@/lib/auth-context"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { SidebarTrigger } from "@/components/ui/sidebar"

import { CommandMenu } from "./command-menu"

export function AppHeader() {
  const { setTheme } = useTheme()
  const { user, logout } = useAuth()

  return (
    <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4 bg-background">
      <SidebarTrigger className="-ml-1" />
      <div className="w-full flex items-center justify-between">
        <div className="flex items-center gap-2">
          <CommandMenu />
        </div>
        <div className="flex items-center gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger render={
              <Button variant="ghost" size="icon" className="rounded-full">
                <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                <span className="sr-only">Toggle theme</span>
              </Button>
            } />
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => setTheme("light")}>
                <Sun className="mr-2 h-4 w-4" />
                <span>Light</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setTheme("dark")}>
                <Moon className="mr-2 h-4 w-4" />
                <span>Dark</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => setTheme("system")}>
                <Monitor className="mr-2 h-4 w-4" />
                <span>System</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {user && (
            <DropdownMenu>
              <DropdownMenuTrigger render={
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <div className="flex h-full w-full items-center justify-center rounded-full bg-primary/10 text-primary">
                    {user.first_name ? user.first_name.charAt(0).toUpperCase() : <User className="h-4 w-4" />}
                  </div>
                </Button>
              } />
              <DropdownMenuContent className="w-56" align="end">
                <div className="flex items-center justify-start gap-2 p-2">
                  <div className="flex flex-col space-y-1 leading-none">
                    {user.first_name && <p className="font-medium">{user.first_name} {user.last_name}</p>}
                    <p className="w-[200px] truncate text-sm text-muted-foreground">
                      {user.email}
                    </p>
                  </div>
                </div>
                <DropdownMenuItem onClick={logout} className="text-red-600 focus:text-red-600">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>
    </header>
  )
}
