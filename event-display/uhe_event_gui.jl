println("Loading libaries...")

using RainbowAlga
using KM3io
using GLMakie
using ColorSchemes
using LinearAlgebra
using GeometryBasics
using FileIO


function main()
    println("Creating scene...")
    setfps!(20)

    RainbowAlga.displayparams.size = (550, 650)
    RainbowAlga._rba.simparams.hit_scaling = 10
    RainbowAlga._rba.simparams.speed = 6
    RainbowAlga._rba.simparams.min_tot = 0
    RainbowAlga._rba.simparams.frame_idx = 0

    println("Loading detector geometry")
    detector = Detector("../data/supplementary/detector/detector.dynamical.datx")
    RainbowAlga.update!(detector)

    println("Reading event data")
    f = ROOTFile("../data/event/KM3-230213A_allhits.root")
    event = first(f.offline)
    muon = bestjppmuon(event)

    # excluding a malfunctioning PMT
    hits = filter(h->h.dom_id != 808950076 && h.channel_id != 3, event.hits)

    hits = select_first_hits(hits; n=5, maxtot=256)

    add!(hits; hit_distance=3)
    add!(hits; hit_distance=3)
    add!(hits; hit_distance=3)
    fhits = select_first_hits(hits; n=1, maxtot=256)
    add!(fhits)
    add!(muon; with_cherenkov_cone=true)

    t₀ = muon.t + 800
    timespan = 1800

    cmap = ColorSchemes.thermal
    cmap_alternative = reverse(ColorSchemes.jet1)

    println("Generating colour schemes")
    # Alternative colourings, use the "C" key to cycle through them
    recolor!(1,  generate_colors(muon, hits; cherenkov_thresholds=(-5, 25), t₀=t₀, timespan=timespan, cmap=cmap))
    recolor!(2,  generate_colors(muon, hits; cherenkov_thresholds=(NaN, NaN), t₀=t₀, timespan=timespan, cmap=cmap))
    recolor!(3,  generate_colors(muon, hits; cherenkov_thresholds=(NaN, NaN), t₀=t₀, timespan=timespan, cmap=cmap_alternative))
    recolor!(4,  generate_colors(muon, fhits; cherenkov_thresholds=(NaN, NaN), t₀=t₀, timespan=timespan, cmap=cmap))
    RainbowAlga._rba.simparams.t_offset = t₀

    draw_cascades(muon, (199, 297, 477))
    draw_compass(Point3f(150, 500, 1), 40)
    draw_scale(Point3d(50, 600, 1), 100)
    draw_eiffel_tower(Point3f(-150, 630, 0))

    # front view
    save_perspective(1, Vec3f(391.5, 1411.7, 1127.7), Vec3f(73.0, 323.8, 380.1))
    # top view
    save_perspective(2, Vec3f(76.3, 640.4, 1631.5), Vec3f(75.8, 324.6, 379.8))
    # zoom
    save_perspective(3, Vec3f(392.9, 634.0, 449.7), Vec3f(70.4, 392.8, 284.1))

    println("Starting the RainbowAlga GUI")
    # setting interactive=true will return to prompt when launched from the REPL
    RainbowAlga.run(;interactive=false)  
end


"""
    draw_compass()

Draws a compass pointing towards (0, 1, 0), which is north.

"""
function draw_compass(pos, size)
    text!(global_scene(), pos + Point3f(0.0, -size/2, 0.0); text = "N", markerspace=:data, font=:bold, fontsize=size*0.8, color=:black, align=(:center, :bottom))
    xyz = [
        Point3f(-1, 0, 0),
        Point3f(0, 2.5, 0),
        Point3f(1, 0, 0),
        Point3f(0, 0.6, 0),
    ] * size
    xyz .+= pos
    xy = Point2f.(xyz)
    f =  faces(Polygon(xy))
    m = GeometryBasics.Mesh(Point3f.(xyz), f)
    mesh!(global_scene(), m; color = :red)
end


"""
    draw_scale()

Draws a scale.

"""
function draw_scale(pos, length)
    opts = Dict(:color => :black, :linewidth => 2)
    lines!(global_scene(), [pos + Point3d(length/2, 10, 0), pos + Point3d(length/2, -10, 0)]; opts...)
    lines!(global_scene(), [pos - Point3d(length/2, -10, 0), pos - Point3d(length/2, 10, 0)]; opts...)
    lines!(global_scene(), [pos - Point3d(length/2, 0, 0), pos + Point3d(length/2, 0, 0)]; opts...)
    text!(global_scene(), pos + Point3d(0.0, -10, 0.0); text = "$(length) m", markerspace=:data, font=:bold, fontsize=23, color=:black, align=(:center, :bottom), rotation=deg2rad(180))
end


"""
    draw_cascades()

Draws the secondary cascade positions along the muon track.

"""
function draw_cascades(muon, cascade_positions)
    meshscatter!(
        global_scene(),
        [muon.pos + muon.dir*i for i in cascade_positions],
        color = [:black for _ in length(cascade_positions)],
        markersize = 5,
        marker = :Sphere,
        alpha = 0.9
    )
end


"""
    draw_eiffel_tower()

Draws the Eiffel tower.

"""
function draw_eiffel_tower(pos)
    eiffel = load("assets/eiffel.stl")

    # The height of the Eiffel Tower with tip is 330m
    scale_factor = 330 / maximum([p[3] for p in eiffel.position])  
    eiffel.position .*= scale_factor
    eiffel.position .+= pos

    # Eiffel Tower Colour from https://encycolorpedia.com/9a8e83
    mesh!(global_scene(), eiffel; color = RGBAf(0.6039, 0.5569, 0.5137, 0.3))  
end


main()
