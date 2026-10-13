local toolbar = plugin:CreateToolbar("T-BloxStudio")
local openButton = toolbar:CreateButton(
	"OpenAppearance",
	"Abrir personalizacao do T-BloxStudio",
	""
)

local widgetInfo = DockWidgetPluginGuiInfo.new(
	Enum.InitialDockState.Float,
	false,
	false,
	320,
	300,
	280,
	260
)

local widget = plugin:CreateDockWidgetPluginGuiAsync("TBloxStudio.Appearance", widgetInfo)
widget.Title = "T-BloxStudio | Aparencia"

local palettes = {
	Carbon = {
		background = Color3.fromRGB(23, 26, 31),
		surface = Color3.fromRGB(34, 39, 47),
		border = Color3.fromRGB(57, 65, 76),
		accent = Color3.fromRGB(183, 239, 109),
		text = Color3.fromRGB(241, 244, 237),
		muted = Color3.fromRGB(158, 168, 177),
	},
	Mint = {
		background = Color3.fromRGB(17, 37, 40),
		surface = Color3.fromRGB(27, 53, 56),
		border = Color3.fromRGB(49, 82, 82),
		accent = Color3.fromRGB(102, 220, 193),
		text = Color3.fromRGB(233, 246, 240),
		muted = Color3.fromRGB(157, 190, 181),
	},
	Coral = {
		background = Color3.fromRGB(43, 29, 28),
		surface = Color3.fromRGB(59, 40, 37),
		border = Color3.fromRGB(91, 59, 52),
		accent = Color3.fromRGB(255, 153, 111),
		text = Color3.fromRGB(255, 239, 229),
		muted = Color3.fromRGB(198, 164, 151),
	},
}

local function create(className, properties, parent)
	local instance = Instance.new(className)
	for property, value in pairs(properties) do
		instance[property] = value
	end
	instance.Parent = parent
	return instance
end

local selectedPalette = plugin:GetSetting("T-BloxStudio.Palette")
if not palettes[selectedPalette] then
	selectedPalette = "Carbon"
end

local root = create("Frame", {
	Name = "Root",
	Size = UDim2.fromScale(1, 1),
	BorderSizePixel = 0,
}, widget)

local padding = create("UIPadding", {
	PaddingTop = UDim.new(0, 18),
	PaddingBottom = UDim.new(0, 16),
	PaddingLeft = UDim.new(0, 18),
	PaddingRight = UDim.new(0, 18),
}, root)

local title = create("TextLabel", {
	Name = "Title",
	BackgroundTransparency = 1,
	Position = UDim2.fromOffset(0, 0),
	Size = UDim2.new(1, 0, 0, 28),
	Font = Enum.Font.GothamBold,
	Text = "T-BLOX STUDIO",
	TextSize = 20,
	TextXAlignment = Enum.TextXAlignment.Left,
}, root)

local subtitle = create("TextLabel", {
	Name = "Subtitle",
	BackgroundTransparency = 1,
	Position = UDim2.fromOffset(0, 29),
	Size = UDim2.new(1, 0, 0, 20),
	Font = Enum.Font.GothamMedium,
	Text = "PERSONALIZACAO",
	TextSize = 11,
	TextXAlignment = Enum.TextXAlignment.Left,
}, root)

local divider = create("Frame", {
	Name = "Divider",
	BorderSizePixel = 0,
	Position = UDim2.fromOffset(0, 62),
	Size = UDim2.new(1, 0, 0, 1),
}, root)

local sectionTitle = create("TextLabel", {
	Name = "SectionTitle",
	BackgroundTransparency = 1,
	Position = UDim2.fromOffset(0, 81),
	Size = UDim2.new(1, 0, 0, 22),
	Font = Enum.Font.GothamSemibold,
	Text = "Cor do painel",
	TextSize = 14,
	TextXAlignment = Enum.TextXAlignment.Left,
}, root)

local paletteRow = create("Frame", {
	Name = "PaletteRow",
	BackgroundTransparency = 1,
	Position = UDim2.fromOffset(0, 115),
	Size = UDim2.new(1, 0, 0, 76),
}, root)

local rowLayout = create("UIListLayout", {
	FillDirection = Enum.FillDirection.Horizontal,
	HorizontalAlignment = Enum.HorizontalAlignment.Left,
	SortOrder = Enum.SortOrder.LayoutOrder,
	Padding = UDim.new(0, 6),
}, paletteRow)

local status = create("TextLabel", {
	Name = "Status",
	BackgroundTransparency = 1,
	Position = UDim2.new(0, 0, 1, -24),
	Size = UDim2.new(1, 0, 0, 20),
	Font = Enum.Font.Gotham,
	TextSize = 12,
	TextXAlignment = Enum.TextXAlignment.Left,
}, root)

local paletteButtons = {}

local function applyPalette(name)
	local palette = palettes[name]
	selectedPalette = name
	root.BackgroundColor3 = palette.background
	title.TextColor3 = palette.text
	subtitle.TextColor3 = palette.muted
	divider.BackgroundColor3 = palette.border
	sectionTitle.TextColor3 = palette.text
	status.TextColor3 = palette.muted
	status.Text = "Ativo: " .. name

	for paletteName, controls in pairs(paletteButtons) do
		local isSelected = paletteName == name
		controls.button.BackgroundColor3 = palette.surface
		controls.label.TextColor3 = palette.text
		controls.swatch.BackgroundColor3 = palettes[paletteName].accent
		controls.stroke.Color = isSelected and palette.accent or palette.border
		controls.stroke.Transparency = isSelected and 0 or 1
	end

	plugin:SetSetting("T-BloxStudio.Palette", name)
end

for order, name in ipairs({ "Carbon", "Mint", "Coral" }) do
	local button = create("TextButton", {
		Name = name,
		BackgroundTransparency = 0,
		BorderSizePixel = 0,
		LayoutOrder = order,
		Size = UDim2.new(1 / 3, -4, 0, 76),
		Text = "",
		AutoButtonColor = true,
	}, paletteRow)

	local stroke = create("UIStroke", {
		Thickness = 1,
		Transparency = 1,
	}, button)

	local swatch = create("Frame", {
		Name = "Swatch",
		BorderSizePixel = 0,
		Position = UDim2.new(0.5, -17, 0, 12),
		Size = UDim2.fromOffset(34, 20),
	}, button)

	local label = create("TextLabel", {
		Name = "Label",
		BackgroundTransparency = 1,
		Position = UDim2.new(0, 2, 0, 42),
		Size = UDim2.new(1, -4, 0, 20),
		Font = Enum.Font.GothamMedium,
		Text = name,
		TextSize = 12,
	}, button)

	paletteButtons[name] = {
		button = button,
		label = label,
		stroke = stroke,
		swatch = swatch,
	}

	button.Activated:Connect(function()
		applyPalette(name)
	end)
end

applyPalette(selectedPalette)

openButton.Click:Connect(function()
	widget.Enabled = not widget.Enabled
end)