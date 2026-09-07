"""Resource handlers for LearnUpon Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListCourseParams, GetCourseParams,
    CourseRecord, CourseList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_courses", "List courses in LearnUpon.", action_type="read", chain_callable=True, event="learnupon-connector.list_courses", effects=["read:courses"], data_model=CourseList)
async def list_courses(ctx, params: ListCourseParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_courses(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.success({"courses": items, "total": len(items)}, summary=f"Found {len(items)} courses.")
    except Exception as e:
        return ActionResult.error(f"Error listing courses: {e}")

@chat.function("get_course", "Get details of one Course in LearnUpon.", action_type="read", chain_callable=True, event="learnupon-connector.get_course", effects=["read:course"], data_model=CourseRecord)
async def get_course(ctx, params: GetCourseParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_course(params.course_id)
        rid = str(r.get("id") or params.course_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.success({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved Course {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving Course: {e}")

@chat.function("audit_course_health", "Audit health of LearnUpon courses and connectivity.", action_type="read", chain_callable=True, event="learnupon-connector.audit_course_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_course_health(ctx, params: ConnectionIdParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_courses(limit=50)
        return ActionResult.success({
            "healthy": True,
            "total_courses": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"LearnUpon healthy. Sampled {len(items)} courses."
        }, summary=f"LearnUpon health check passed with {len(items)} courses.")
    except Exception as e:
        return ActionResult.error(f"Error auditing LearnUpon health: {e}")
