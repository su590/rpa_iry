# -*- coding: utf-8 -*-
"""
@Date     : 2025-03-20
@Author   : xwq
@Desc     : iry定时调度
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

from src.service.run_iry import main


def _iry_timeframe() -> None:
    """
    iry时段任务
    """
    try:
        logging.info("iry定时任务开始执行")
        main()
        logging.info("iry定时任务执行完成")
    except Exception as e:
        logging.error("iry定时任务执行失败: %s", e)


def create_scheduler() -> BlockingScheduler:
    scheduler = BlockingScheduler()

    # 1. 每天 10:00 - 23:30，每半小时执行一次
    scheduler.add_job(
        _iry_timeframe,
        trigger=CronTrigger(hour="10-23", minute="0,30"),
        id="iry_half_hour",
        misfire_grace_time=300,  # 允许 5 分钟内补跑
        max_instances=1,
        replace_existing=True
    )

    # 2. 每天 23:50 再跑一次
    scheduler.add_job(
        _iry_timeframe,
        trigger=CronTrigger(hour=23, minute=50),
        id="iry_2350",
        misfire_grace_time=300,
        max_instances=1,
        replace_existing=True
    )

    return scheduler


def create_scheduler_and_start():
    scheduler = create_scheduler()
    logging.info("启动 iry 定时调度器")
    scheduler.start()


if __name__ == '__main__':
    create_scheduler_and_start()
