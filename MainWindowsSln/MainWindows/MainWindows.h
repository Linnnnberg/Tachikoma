#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_MainWindows.h"

class MainWindows : public QMainWindow
{
	Q_OBJECT

public:
	MainWindows(QWidget *parent = Q_NULLPTR);

private:
	Ui::MainWindowsClass ui;
};
