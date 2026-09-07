# Thin wrapper around dashboard.sh so day-to-day commands read as
# `make dev` / `make down` instead of `./dashboard.sh up` / `./dashboard.sh down`.
# All the actual logic (Docker vs. local fallback, the facilitator link,
# ADR-0022's lifecycle) lives in dashboard.sh — this just names the targets.

.DEFAULT_GOAL := help

.PHONY: help dev down rebuild logs local

help:
	@echo "make dev      build + start the dashboard (Docker), opens your browser"
	@echo "make down     stop the dashboard"
	@echo "make rebuild  clean rebuild, then start"
	@echo "make logs     follow the dashboard's container logs"
	@echo "make local    run Flask directly, no Docker (workshop-laptop fallback)"

dev:
	./dashboard.sh up

down:
	./dashboard.sh down

rebuild:
	./dashboard.sh rebuild

logs:
	./dashboard.sh logs

local:
	./dashboard.sh local
